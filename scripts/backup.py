#!/usr/bin/env python3
"""Private, file-scoped snapshots. Never traverse a symlinked parent directory."""
import argparse
import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def validate_path(home, relative):
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts or relative in ('', '.'):
        raise ValueError(f'Unsafe snapshot path: {relative}')
    target = home / rel
    for parent in target.parents:
        if parent == home:
            break
        if parent.is_symlink():
            raise ValueError(f'Migrate symlinked parent before applying: {parent}')
    if target.is_dir() and not target.is_symlink():
        raise ValueError(f'Expected a file, found a directory: {target}')
    return target


def snapshot(home, paths, root=None):
    paths = sorted(set(paths))
    targets = [(p, validate_path(home, p)) for p in paths]
    root = root or home / '.local/state/dotfiles/backups'
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    root.chmod(0o700)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ-')
    backup = Path(tempfile.mkdtemp(prefix=stamp, dir=root))
    records = []
    for relative, target in targets:
        entry = {'path': relative, 'kind': 'absent'}
        if target.is_symlink():
            entry.update(kind='symlink', link=os.readlink(target))
        elif target.is_file():
            out = backup / 'files' / relative
            out.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            shutil.copy2(target, out)
            entry.update(kind='file')
        records.append(entry)
    (backup / 'manifest.json').write_text(json.dumps({'home': str(home), 'files': records}, indent=2) + '\n')
    return backup


def restore(home, backup):
    manifest = json.loads((backup / 'manifest.json').read_text())
    if manifest['home'] != str(home):
        raise ValueError('Snapshot belongs to another home directory')
    records = manifest['files']
    for record in records:
        validate_path(home, record['path'])
        if record['kind'] not in ('file', 'symlink', 'absent'):
            raise ValueError('Invalid snapshot entry')
        if record['kind'] == 'file' and not (backup / 'files' / record['path']).is_file():
            raise ValueError('Snapshot is incomplete')
    # Rollback is itself reversible.
    safety = snapshot(home, [r['path'] for r in records])
    print(f'Pre-restore snapshot: {safety}')
    for record in records:
        target = validate_path(home, record['path'])
        if target.is_symlink() or target.is_file():
            target.unlink()
        if record['kind'] == 'absent':
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if record['kind'] == 'symlink':
            target.symlink_to(record['link'])
        else:
            shutil.copy2(backup / 'files' / record['path'], target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['config', 'snapshot', 'restore'])
    parser.add_argument('backup', nargs='?', type=Path)
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--home', type=Path, default=Path.home())
    args = parser.parse_args()
    home = args.home.absolute()
    if args.action == 'restore':
        if args.backup is None:
            parser.error('restore requires a snapshot directory')
        restore(home, args.backup)
        return
    if args.action == 'config':
        config_home = Path(os.environ.get('XDG_CONFIG_HOME', home / '.config'))
        paths = [str((config_home / 'chezmoi/chezmoi.toml').relative_to(home))]
    else:
        result = subprocess.check_output([
            'chezmoi', '--source', str(args.source), '--destination', str(home),
            'managed', '--include=files,symlinks', '--nul-path-separator', '--path-style=relative',
        ], text=True)
        paths = [path for path in result.split('\0') if path]
    print(f'Snapshot: {snapshot(home, paths)}')


if __name__ == '__main__':
    main()
