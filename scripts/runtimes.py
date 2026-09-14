#!/usr/bin/env python3
"""Install the captured runtimes with fnm/ruby-install; keep existing selections."""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    versions = json.loads((root / 'packages/runtimes.json').read_text())
    if not args.apply:
        print(json.dumps(versions, indent=2))
        print('Preview only. --apply installs missing versions using the existing managers.')
        return
    subprocess.run(['fnm', 'install', versions['node']], check=True)
    default = subprocess.run(['fnm', 'default'], capture_output=True, text=True)
    if default.returncode != 0 or not default.stdout.strip():
        subprocess.run(['fnm', 'default', versions['node']], check=True)
    npm = ['fnm', 'exec', '--using', versions['node'], '--', 'npm']
    result = subprocess.run(npm + ['ls', '--global', '--depth=0', '--json'], capture_output=True, text=True)
    installed = json.loads(result.stdout).get('dependencies', {})
    for name, version in versions['npm'].items():
        if name not in installed:
            subprocess.run(npm + ['install', '--global', f'{name}@{version}'], check=True)
    if 'corepack' not in installed:
        subprocess.run(['fnm', 'exec', '--using', versions['node'], '--', 'corepack',
                        'install', '--global', f"pnpm@{versions['pnpm']}"], check=True)
    home = Path.home()
    if not (home / '.bun/bin/bun').exists():
        subprocess.run(npm + ['install', '--global', '--prefix', str(home / '.bun'), f"bun@{versions['bun']}"], check=True)
    if not (home / '.rubies' / f"ruby-{versions['ruby']}" / 'bin/ruby').exists():
        subprocess.run(['ruby-install', '--no-reinstall', 'ruby', versions['ruby']], check=True)
    # No chruby selection, corepack activation, or shell profile writes here.


if __name__ == '__main__':
    main()
