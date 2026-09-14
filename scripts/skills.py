#!/usr/bin/env python3
"""Preview public skill installation; --apply installs via the pinned skills CLI."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import shlex
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--apply', action='store_true')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
groups = defaultdict(list)
for name, entry in json.loads((root / 'packages/agent-skills.json').read_text()).items():
    groups[entry['source']].append(name)
for source, names in sorted(groups.items()):
    command = ['npx', '--yes', '--registry=https://registry.npmjs.org', 'skills@1.5.26',
               'add', f'https://github.com/{source}', '--global', '--agent', 'codex', 'claude-code',
               '--skill', *sorted(names), '--yes']
    print(shlex.join(command), flush=True)
    if args.apply:
        subprocess.run(command, check=True)
