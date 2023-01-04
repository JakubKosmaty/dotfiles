from __future__ import annotations

import argparse
import platform
from enum import Enum
from pathlib import Path

import ruamel.yaml
from pydantic import BaseModel
from pydantic import validator

CONFIG_PATH = 'dotfiles-mapping.yml'
USER_OS = platform.system()

yaml = ruamel.yaml.YAML(typ='safe')


class OS(str,  Enum):
    linux = 'Linux'
    windows = 'Windows'
    independent = 'Independent'


class Link(BaseModel):
    file: Path
    link_to: Path
    os = OS.independent

    @validator('file')
    def check_if_exists_and_resolve_file(cls, v: Path) -> Path:
        if not v.exists():
            raise ValueError(f'File does not exists: {v}')
        return v.resolve()

    @validator('link_to')
    def expand_link(cls, v: Path) -> Path:
        return v.expanduser()

    def symlink(self) -> None:
        parent = self.link_to.parent
        parent.mkdir(parents=True, exist_ok=True)

        try:
            self.link_to.symlink_to(self.file)
            print(f'Link successfully created: {self}')
        except OSError as err:
            print(f'Could not create symlink ({self}): {err}')

    def unlink(self) -> None:
        self.link_to.unlink(missing_ok=True)

    def is_for_user_os(self) -> bool:
        os = self.os
        return os == OS.independent or os == USER_OS

    def is_exists(self) -> bool:
        return self.link_to.exists() or self.link_to.is_symlink()

    def __str__(self) -> str:
        return f'{self.link_to} -> {self.file}'


class Config(BaseModel):
    force_creation: bool
    links: list[Link]


def parse_config(config: str) -> Config:
    path = Path(config)
    contents = yaml.load(path)
    to_dict = dict(contents)
    return Config.parse_obj(to_dict)


def create_symlinks(config: Config) -> None:
    force = config.force_creation
    for link in config.links:
        if not link.is_for_user_os():
            continue

        if not force and link.is_exists():
            print(f'Link or file already exists: {link.link_to}')
            continue

        link.unlink()
        link.symlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        default=CONFIG_PATH,
        help='Path to config file',
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path: str = args.config
    config = parse_config(config_path)
    create_symlinks(config)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
