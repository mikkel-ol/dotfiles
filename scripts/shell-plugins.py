#!/usr/bin/env python3
"""Install missing original zsh dependencies without running shell installers."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def install(entry, home):
    target = home / entry['path']
    # Existing installations, including uncommitted customization, are untouched.
    if (target / '.git').exists():
        print(f'Keeping existing {target}')
        return
    # chezmoi may already have created only the custom-theme subtree.
    if target.exists() and entry['path'] != '.oh-my-zsh':
        print(f'Keeping existing {target}')
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='dotfiles-plugin-') as directory:
        staged = Path(directory) / 'checkout'
        subprocess.run(['git', 'init', '-q', str(staged)], check=True)
        subprocess.run(['git', '-C', str(staged), 'fetch', '--depth=1', entry['url'], entry['commit']], check=True)
        subprocess.run(['git', '-C', str(staged), 'checkout', '--detach', 'FETCH_HEAD'], check=True)
        # Merge only missing files. Never overwrite the custom theme or user edits.
        for source in sorted(staged.rglob('*')):
            dest = target / source.relative_to(staged)
            if dest.exists() or dest.is_symlink():
                continue
            if source.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest, follow_symlinks=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    for entry in json.loads((root / 'packages/shell-plugins.json').read_text()):
        print(f"{entry['path']} <- {entry['url']} @ {entry['commit']}")
        if args.apply:
            install(entry, Path.home())


if __name__ == '__main__':
    main()
