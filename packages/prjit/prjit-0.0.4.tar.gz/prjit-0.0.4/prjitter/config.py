from os import getenv
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field, field_validator


class GlobalConfig(BaseModel):
    root_dir: str = Field(description="The root directory of prjit. Please set PRJIT_ROOT_DIR environment variable")

    @classmethod
    def load_from_env(cls) -> 'GlobalConfig':
        home_dir = getenv("HOME", "")
        home_dir_path = Path(home_dir)
        default_prjit_root_dir_path = home_dir_path / ".prjit"
        prjit_root_dir = getenv("PRJIT_ROOT_DIR", str(default_prjit_root_dir_path.absolute()))
        prjit_root_dir_path = Path(prjit_root_dir).absolute()
        return cls(root_dir=str(prjit_root_dir_path))

    def root_path(self):
        return Path(self.root_dir)

    def switch_log_path(self) -> Path:
        return self.root_path() / 'switch.log'


class PrjitSwitchPath(BaseModel):
    name: str = Field(description="The name of the switch path")
    path: str = Field(description="The path of the switch path")
    is_directory: bool = Field(description="Whether the switch path is a directory", default=True)

    def __str__(self) -> str:
        return f"{self.name}: {self.path}"

    @field_validator("path")
    @classmethod
    def validate_path_availability(cls, v: str) -> str:
        path = Path(v)
        if not path.is_absolute():
            raise ValueError("Path must be absolute")
        if not path.parent.exists():
            raise ValueError("Path parent does not exist")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        validation = v.isalnum() or (v in ("_", "-", "."))
        if not validation:
            raise ValueError("Name must be alphanumeric, `_`, `-` or `.`.")
        return v

    def switch_src_path(self, global_config: GlobalConfig, prjit_config: 'PrjitConfig') -> Path:
        switch_root_path = prjit_config.switch_root_path(global_config)
        return switch_root_path / self.name

    def switch_dst_path(self) -> Path:
        return Path(self.path)


class PrjitConfig(BaseModel):
    project_name: str = Field(description="The name of the project", default="default")
    switch_paths: list[PrjitSwitchPath] = Field(description="The paths to be switched by prjit", default=[])
    is_default: bool = Field(description="Whether the project is the default project", default=True)
    auto_bind_bundle_ids: list[str] = Field(description="The bundle ids to be auto bound", default=[])

    def config_file_path(self, global_config: GlobalConfig) -> Path:
        return self.config_file_path_by_name(global_config, self.project_name)

    @classmethod
    def config_file_path_by_name(cls, global_config: GlobalConfig, name: str) -> Path:
        return Path(global_config.root_dir) / f"{name}.yml"

    def dump(self, global_config: GlobalConfig) -> None:
        destination = self.config_file_path(global_config)
        content_dict = self.dict()
        print(f'Writing prjit config {self.project_name} to {str(destination)}')
        with destination.open('w') as f:
            try:
                yaml.dump(content_dict, f, default_flow_style=False, allow_unicode=True)
            except Exception as e:
                print(f'Failed to write prjit config {self.project_name} to {str(destination)}')
                print(e)
                return

    @classmethod
    def load(cls, global_config: GlobalConfig, name: str) -> Optional['PrjitConfig']:
        source = cls.config_file_path_by_name(global_config, name)
        if not source.exists():
            print(f'Failed to load prjit config {name} from {str(source)}')
            return
        with source.open() as f:
            try:
                content_dict = yaml.safe_load(f)
                return cls(**content_dict)
            except Exception as e:
                print(f'Failed to load prjit config {name} from {str(source)}')
                print(e)
                return

    def switch_root_path(self, global_config: GlobalConfig) -> Path:
        global_root_path = global_config.root_path()
        return global_root_path / self.project_name

    def create_switch_root_path(self, global_config: GlobalConfig):
        print('Creating new switch root path for project:', self.project_name)
        root_path = self.switch_root_path(global_config)
        root_path.mkdir(parents=False, exist_ok=False)
