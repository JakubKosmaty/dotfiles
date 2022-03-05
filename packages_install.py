import sys
import json
import argparse
import subprocess
from typing import Callable


MAP_MANAGER_TO_FUNC: dict[str, Callable[[str], None]] = {}


def extract_packages(manager: str) -> list[str]:
    with open('packages.json', 'r') as f:
        data = json.load(f)
        return data[manager]


def _subprocess_check_call(cmd: tuple) -> None:
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        sys.exit(f'Error while executing command: {e}')


def register_manager(f: Callable[[str], None]):
    return MAP_MANAGER_TO_FUNC.setdefault(f.__name__, f)


@register_manager
def choco(name: str) -> None:
    _subprocess_check_call(('choco', 'install', '-y', name))


@register_manager
def apt(name: str) -> None:
    _subprocess_check_call(('apt-get', 'install', '-y', name))


@register_manager
def powershell(name: str) -> None:
    _subprocess_check_call(
        ('Install-Module', '-Scope', 'CurrentUser', '-Name', name))


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'package_manager',
        choices=MAP_MANAGER_TO_FUNC.keys(),
        help='Install modules from "packages.json"'
    )

    return parser.parse_args()


def main():
    args = parse_args()
    manager = args.package_manager
    packages = extract_packages(manager)

    any(MAP_MANAGER_TO_FUNC[manager](x) for x in packages)


if __name__ == "__main__":
    main()
