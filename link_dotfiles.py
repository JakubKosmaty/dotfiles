from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path


def detect_os() -> str:
    os = platform.system()
    if os not in ['Windows', 'Linux']:
        raise SystemExit(f'Unsupported OS(Allowed: Windows, Linux): {os}')
    return os


def extract_mapping(os: str) -> dict[str, str]:
    with open('dotfiles-mapping.json') as f:
        data = json.load(f)
        # return data[os] | data['Shared']
        return {**data[os], **data['Shared']}


def link(target: str, link: str, force: bool) -> int:
    target_path = Path(target).resolve()
    if not target_path.is_file():
        print(
            f'Could not link(Reason: {target} does not exists):'
            f'{link} -> {target}',
        )
        return 1

    link_path = Path(link).expanduser()
    if link_path.exists():
        if not force:
            print(f'Link already exists(Use flag -f): {link_path}')
            return 1

        link_path.unlink()

    parent = link_path.parent
    parent.mkdir(parents=True, exist_ok=True)

    try:
        link_path.symlink_to(target_path)
        print(f'Successfully created symlink: {link_path} --> {target_path}')
    except OSError as err:
        print(f'Internal OS Error: {err}')

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='If symlink or file already exists, remove it and create symlink',
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    force: bool = args.force

    os = detect_os()
    mapping = extract_mapping(os)

    return any(link(k, v, force) for k, v in mapping.items())


if __name__ == '__main__':
    raise SystemExit(main())
