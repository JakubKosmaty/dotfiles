import sys
import json
import argparse
import platform
from pathlib import Path


def detect_os() -> str:
    os = platform.system()
    if os not in ['Windows', 'Linux']:
        sys.exit(f'Unsupported OS(Allowed: Windows, Linux): {os}')
    return os


def extract_mapping(os: str) -> dict[str, str]:
    with open('dotfiles-mapping.json', 'r') as f:
        data = json.load(f)
        return data[os] | data['Shared']


def link(target: str, link: str, force: bool) -> None:
    target_path = Path(target).resolve()
    if not target_path.is_file():
        print(f'Could not link(Reason: {target} does not exists): {link} --> {target}')
        return

    link_path = Path(link).expanduser()
    if link_path.exists():
        if not force:
            print(f'Link already exists(Use flag -f): {link_path}')
            return

        link_path.unlink()

    parent = link_path.parent
    parent.mkdir(parents=True, exist_ok=True)

    try:
        link_path.symlink_to(target_path)
        print(f'Successfully created symlink: {link_path} --> {target_path}')
    except OSError as err:
        print(f'Internal OS Error: {err}')


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
    mapping = extract_mapping(os)

    any(link(k, v, force) for k, v in mapping.items())


if __name__ == "__main__":
    main()
