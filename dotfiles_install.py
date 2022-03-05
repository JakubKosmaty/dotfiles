import sys
import json
import argparse
import platform
from pathlib import Path


def detect_os() -> str:
    os = platform.system()
    if os not in ['Windows', 'Linux']:
        sys.exit(f'Unsupported OS: {os}')
    return os


def extract_os_symlinks(os: str) -> dict[str, str]:
    with open('symlinks.json', 'r') as f:
        data = json.load(f)
        return data[os]


def create_symlink(link: Path, target: Path) -> None:
    try:
        link.symlink_to(target)
        print(f'Successfully created symlink: {link} --> {target}')
    except FileExistsError as err:
        raise err
    except FileNotFoundError as err:
        print(f'Could not create symlink: {err}')
    except OSError as err:
        print(f'OS error: {err}')


def link(target: str, link: str, force: bool) -> None:
    target_path = Path(target).resolve()
    if not target_path.is_file():
        print(f'File does not exists: {target_path}')
        return

    link_path = Path(link).expanduser()

    try:
        create_symlink(link_path, target_path)
    except FileExistsError as err:
        if force:
            link_path.unlink()
            create_symlink(link_path, target_path)
        else:
            print(f'Could not create symlink: {err}')


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='If symlink or file already exists, remove it and create symlink'
    )

    return parser.parse_args()


def main():
    args = parse_args()
    force: bool = args.force

    os = detect_os()
    symlinks = extract_os_symlinks(os)

    any(link(k, v, force) for k, v in symlinks.items())


if __name__ == "__main__":
    main()
