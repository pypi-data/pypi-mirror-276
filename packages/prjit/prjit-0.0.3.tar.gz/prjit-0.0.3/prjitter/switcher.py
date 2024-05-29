from prjitter.bundles import BundleManager
from prjitter.config import PrjitSwitchPath
from prjitter.state import PrjitState


class PlanError(Exception):
    pass


class PrjitSwitcher:
    def __init__(self, state: PrjitState):
        self.state = state

    def plan_switch_in(self, name: str):
        switch_out_commands = self.plan_switch_out()
        switch_in_commands = self.plan_mount_paths(name)
        return switch_out_commands + switch_in_commands

    def plan_switch_out(self) -> list[list[str]]:
        if self.state.current_project is None:
            print('No project mounted')
            return []
        commands = self.plan_unmount_paths()
        commands += self.plan_kill_bundles()
        return commands

    def plan_mount_paths(self, project_name: str) -> list[list[str]]:
        project = self.state[project_name]
        commands = []
        for switch_path in project.switch_paths:
            source_path = switch_path.switch_src_path(self.state.global_config, project)
            destination_path = switch_path.switch_dst_path()
            if destination_path.exists():
                print(f"Path {destination_path} exists. Please check it will be unmounted.")
            commands.append(['ln', '-s', str(source_path), str(destination_path)])
        return commands

    def plan_unmount_paths(self) -> list[list[str]]:
        mounted_project_name = self.state.current_project
        mounted_project = self.state[mounted_project_name]
        commands = []
        for switch_path in mounted_project.switch_paths:
            commands.append(['rm', '-f', str(switch_path.path)])
        return commands

    def plan_kill_bundles(self) -> list[list[str]]:
        mounted_project_name = self.state.current_project
        mounted_project = self.state[mounted_project_name]
        temp_bind_bundles = self.state.bound_bundle_ids
        permanent_bind_bundles = mounted_project.auto_bind_bundle_ids
        bundles_to_kill = list(set(temp_bind_bundles) | set(permanent_bind_bundles))
        bundle_processes = BundleManager().find_all_bundles(bundles_to_kill)
        commands = []
        for bundle_process in bundle_processes:
            commands.append(['kill', str(bundle_process.pid)])
        return commands

    def plan_add_switch_path(self, switch_path: PrjitSwitchPath, create_backup: bool = True):
        mounted_project_name = self.state.current_project
        mounted_project = self.state[mounted_project_name]
        original_path = switch_path.switch_dst_path()
        move_to_path = switch_path.switch_src_path(self.state.global_config, mounted_project)
        commands = []
        if original_path.exists():
            if create_backup:
                backup_path = original_path.with_suffix('.bak')
                commands.append(['cp', str(original_path), str(backup_path)])
            commands.append(['mv', str(original_path), str(move_to_path)])
        elif switch_path.is_directory:
            commands.append(['mkdir', '-p', str(move_to_path)])
        else:
            commands.append(['touch', str(move_to_path)])
        commands.append(['ln', '-s', str(move_to_path), str(original_path)])
        return commands

    def plan_remove_switch_path(self, switch_path: PrjitSwitchPath, restore: bool = True):
        mounted_project_name = self.state.current_project
        mounted_project = self.state[mounted_project_name]
        symbolic_link_path = switch_path.switch_dst_path()
        actual_path = switch_path.switch_src_path(self.state.global_config, mounted_project)
        commands = [['rm', '-f', str(symbolic_link_path)]]
        if restore:
            if not actual_path.exists():
                print(f'Path {actual_path} does not exist. Cannot restore.')
                raise PlanError(f'Path {actual_path} does not exist. Cannot restore.')
            commands.append(['mv', str(actual_path), str(symbolic_link_path)])
        return commands
