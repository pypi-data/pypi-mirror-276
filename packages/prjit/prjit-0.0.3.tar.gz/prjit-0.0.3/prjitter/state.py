from typing import Optional

import yaml
from pydantic import BaseModel, Field

from prjitter.config import GlobalConfig, PrjitConfig


class PrjitState(BaseModel):
    global_config: GlobalConfig
    project_configs: list[PrjitConfig]
    default_project: str
    current_project: Optional[str] = Field(default=None)
    bound_bundle_ids: list[str] = Field(default=[])

    @classmethod
    def load_config(cls, global_config: GlobalConfig) -> Optional['PrjitState']:
        root_path = global_config.root_path()
        if not root_path.exists():
            print(f'prjit root dir does not exist: {str(root_path)}')
            return
        project_configs = []
        config_files = root_path.glob("*.yml")
        for config_file in config_files:
            project_config = PrjitConfig.load(global_config, config_file.stem)
            if project_config:
                project_configs.append(project_config)

        default_project = None
        for project_config in project_configs:
            if project_config.is_default:
                if default_project is not None:
                    print('Multiple default projects found:', default_project, project_config.project_name)
                    return
                default_project = project_config.project_name

        if default_project is None:
            print('No default project found')
            return

        current_project = None
        bound_bundle_ids = []
        current_path_file = root_path / 'current'
        if current_path_file.exists():
            with current_path_file.open() as f:
                try:
                    content_dict = yaml.safe_load(f)
                    current_project = content_dict['current_project']
                    if current_project == "":
                        current_project = None
                    bound_bundle_ids = content_dict.get('bound_bundle_ids', [])
                    if not isinstance(bound_bundle_ids, list):
                        bound_bundle_ids = []
                except Exception as e:
                    print(f'Failed to load prjit state from {str(current_path_file)}')
                    print(e)
        if current_project == "":
            current_project = None
        if (current_project is not None) and \
                (current_project not in [project.project_name for project in project_configs]):
            print(f'Current project {current_project} not found in project configs')
            current_project = None

        return cls(global_config=global_config,
                   project_configs=project_configs,
                   default_project=default_project,
                   current_project=current_project,
                   bound_bundle_ids=bound_bundle_ids)

    def save_current(self):
        destination = self.global_config.root_path() / 'current'
        content_dict = {'current_project': self.current_project, 'bound_bundle_ids': self.bound_bundle_ids}
        print(f'Writing prjit state to {str(destination)}')
        with destination.open('w') as f:
            try:
                yaml.dump(content_dict, f, default_flow_style=False, allow_unicode=True)
            except Exception as e:
                print(f'Failed to write prjit state to {str(destination)}')
                print(e)
                return

    def __getitem__(self, project_name: str) -> PrjitConfig:
        for project_config in self.project_configs:
            if project_config.project_name == project_name:
                return project_config
        raise KeyError(project_name)

    def __contains__(self, project_name: str) -> bool:
        for project_config in self.project_configs:
            if project_config.project_name == project_name:
                return True
        return False
