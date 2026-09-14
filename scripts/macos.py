#!/usr/bin/env python3
"""Preview/apply observed macOS preferences; back up only the keys we manage."""
import argparse
import datetime
import json
import os
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile

DEFAULTS = Path(__file__).resolve().parents[1] / 'macos/defaults.json'


def write(domain, key, value):
    if value is None:
        # Deleting an already absent preference is harmless.
        subprocess.run(['defaults', 'delete', domain, key], capture_output=True)
        return
    if isinstance(value, bool):
        kind, text = '-bool', str(value).lower()
    elif isinstance(value, int):
        kind, text = '-int', str(value)
    elif isinstance(value, str):
        kind, text = '-string', value
    else:
        raise ValueError(f'Unsupported preference type: {domain}/{key}')
    subprocess.run(['defaults', 'write', domain, key, kind, text], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--apply', action='store_true')
    group.add_argument('--restore', type=Path)
    args = parser.parse_args()
    wanted = json.loads((args.restore or DEFAULTS).read_text())
    allowed = json.loads(DEFAULTS.read_text())
    if any(d not in allowed or any(k not in allowed[d] for k in keys) for d, keys in wanted.items()):
        parser.error('Restore contains keys outside the managed allowlist')
    if not args.apply and not args.restore:
        print(json.dumps(wanted, indent=2))
        print('Preview only. Use --apply; log out/in afterwards to activate preferences.')
        return
    if sys.platform != 'darwin':
        parser.error('Applying preferences requires macOS')
    before = {}
    for domain, keys in wanted.items():
        result = subprocess.run(['defaults', 'export', domain, '-'], capture_output=True)
        current = plistlib.loads(result.stdout) if result.returncode == 0 else {}
        before[domain] = {key: current.get(key) for key in keys}
    root = Path.home() / '.local/state/dotfiles/macos'
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    root.chmod(0o700)
    fd, filename = tempfile.mkstemp(prefix=datetime.datetime.now().strftime('%Y%m%d-%H%M%S-'), suffix='.json', dir=root)
    with os.fdopen(fd, 'w') as out:
        json.dump(before, out, indent=2)
    print(f'Preferences backup: {filename}')
    for domain, keys in wanted.items():
        for key, value in keys.items():
            write(domain, key, value)
    print('Preferences applied. Log out/in when convenient.')


if __name__ == '__main__':
    main()
