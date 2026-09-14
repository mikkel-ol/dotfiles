"""Exercise real chezmoi in disposable homes; never apply to the developer's home."""
import importlib.util
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHEZMOI = shutil.which('chezmoi')
spec = importlib.util.spec_from_file_location('backup', ROOT / 'scripts/backup.py')
backup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backup)


class DotfilesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='dotfiles-test-')
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.env = dict(os.environ, HOME=str(self.home))
        for key, subdir in [('XDG_CONFIG_HOME', '.config'), ('XDG_CACHE_HOME', '.cache'),
                            ('XDG_DATA_HOME', '.local/share'), ('XDG_STATE_HOME', '.local/state')]:
            self.env[key] = str(self.home / subdir)
        for key in list(self.env):
            if key.startswith(('GIT_', 'MISE_', 'ZDOTDIR', 'LAZY')):
                del self.env[key]
        self.command = [CHEZMOI, '--source', str(ROOT), '--destination', str(self.home),
                        '--config', str(self.home / '.config/chezmoi/chezmoi.toml'),
                        '--persistent-state', str(self.home / 'state.db'), '--no-tty', '--no-pager']

    def run_cm(self, *args):
        return subprocess.run(self.command + list(args), env=self.env, text=True,
                              capture_output=True, check=True)

    def initialize(self, os_name=None):
        self.run_cm('init', '--promptDefaults', '--recurse-submodules=false')
        if os_name:
            self.command += ['--override-data', json.dumps({'chezmoi': {'os': os_name}})]

    def test_render_and_repeat_apply(self):
        self.initialize()
        self.run_cm('apply', '--force')
        self.run_cm('verify', '--exclude=scripts')
        self.run_cm('apply', '--force')
        self.assertEqual(self.run_cm('diff', '--exclude=scripts').stdout, '')
        managed = self.run_cm('managed', '--include=files', '--nul-path-separator').stdout.split('\0')
        for name in filter(None, managed):
            path = self.home / name
            if not path.is_file() or path.name in ('state.db', 'chezmoi.toml'):
                continue
            text = path.read_text()
            self.assertNotIn('/Users/miu', text, str(path))
            self.assertNotIn('/Users/mikkel', text, str(path))
            if path.suffix == '.toml':
                tomllib.loads(text)
            elif path.suffix in ('.json', '.jsonc'):
                # Captured editor JSONC uses full-line comments and trailing commas.
                clean = re.sub(r'^\s*//.*$', '', text, flags=re.MULTILINE)
                json.loads(re.sub(r',\s*([}\]])', r'\1', clean))
        git_config = self.home / '.gitconfig'
        result = subprocess.check_output(['git', 'config', '--file', str(git_config), 'credential.https://github.com.helper'], text=True)
        self.assertIn('!gh auth git-credential', result)
        self.assertEqual((self.home / '.ssh/config').stat().st_mode & 0o777, 0o600)
        self.assertEqual((self.home / '.codex/config.toml').stat().st_mode & 0o777, 0o600)

    def test_linux_omits_macos_files(self):
        self.initialize('linux')
        self.run_cm('apply', '--force')
        self.assertFalse((self.home / 'Library').exists())
        self.assertFalse((self.home / '.aerospace.toml').exists())
        self.assertFalse((self.home / '.config/karabiner').exists())
        self.assertFalse((self.home / '.docker').exists())
        self.assertTrue((self.home / '.zshrc').exists())
        self.run_cm('verify', '--exclude=scripts')

    def test_existing_private_configs_and_overrides_survive(self):
        self.initialize()
        paths = ['.ssh/config', '.codex/config.toml', '.claude/settings.json',
                 '.config/opencode/opencode.jsonc', '.config/zsh/local.zsh', '.config/git/local.inc']
        for relative in paths:
            p = self.home / relative
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('# local sentinel\n')
        self.run_cm('apply', '--force')
        for relative in paths:
            self.assertEqual((self.home / relative).read_text(), '# local sentinel\n')

    def test_git_work_identity_and_persistent_init(self):
        self.initialize()
        config = self.home / '.config/chezmoi/chezmoi.toml'
        config.write_text(config.read_text().replace('defaultEmail = "m@ikkel.dk"', 'defaultEmail = "work@example.test"'))
        self.run_cm('init', '--promptDefaults', '--recurse-submodules=false')
        self.run_cm('apply', '--force')
        for folder, expected in [('dev/mikkel-ol/project', 'm@ikkel.dk'), ('dev/company/project', 'work@example.test')]:
            path = self.home / folder
            path.mkdir(parents=True)
            subprocess.run(['git', 'init', '-q', str(path)], env=self.env, check=True)
            email = subprocess.check_output(['git', '-C', str(path), 'config', 'user.email'], env=self.env, text=True).strip()
            self.assertEqual(email, expected)
        for setting in ['init.defaultBranch', 'fetch.prune', 'push.autoSetupRemote', 'diff.algorithm',
                        'merge.conflictStyle', 'rerere.enabled', 'core.editor', 'core.excludesFile']:
            result = subprocess.run(['git', 'config', '--file', str(self.home / '.gitconfig'), '--get', setting], capture_output=True)
            self.assertEqual(result.returncode, 1, setting)

    def test_preserved_shell_preferences_and_apply_backup(self):
        self.initialize()
        (self.home / '.zshrc').write_text('# pre-existing user configuration\n')
        self.run_cm('apply', '--force')
        shell = (self.home / '.zshrc').read_text()
        self.assertIn('ZSH_THEME="laksnoster"', shell)
        self.assertIn('  zsh-vi-mode\n', shell)
        self.assertIn('  git-open\n', shell)
        self.assertIn('fnm env --use-on-cd --shell zsh', shell)
        for replacement in ['starship', 'zoxide', 'mise activate', 'HISTSIZE=', 'KEYTIMEOUT=']:
            self.assertNotIn(replacement, shell)
        self.assertIn('alias git=hub', (self.home / '.config/zsh/alias/git.alias.zsh').read_text())
        self.assertIn('zle accept-line', (self.home / '.config/zsh/plugins/git-branches.zsh').read_text())
        self.assertIn('zle accept-line', (self.home / '.config/zsh/plugins/nps.zsh').read_text())
        backups = list((self.home / '.local/state/dotfiles/backups').glob('*/files/.zshrc'))
        self.assertTrue(any(p.read_text() == '# pre-existing user configuration\n' for p in backups))
        self.assertIn('checker = { enabled = true }', (self.home / '.config/nvim/lua/config/lazy.lua').read_text())
        self.assertIn('map cmd+10 goto_tab 10', (self.home / '.config/kitty/kitty.conf').read_text())

    def test_backup_restore_and_parent_symlink_rejection(self):
        (self.home / 'existing').write_text('original')
        (self.home / 'linked').symlink_to('existing')
        snap = backup.snapshot(self.home, ['existing', 'linked', 'new'])
        (self.home / 'existing').write_text('changed')
        (self.home / 'linked').unlink()
        (self.home / 'linked').write_text('replacement')
        (self.home / 'new').write_text('created')
        backup.restore(self.home, snap)
        self.assertEqual((self.home / 'existing').read_text(), 'original')
        self.assertTrue((self.home / 'linked').is_symlink())
        self.assertFalse((self.home / 'new').exists())
        self.assertEqual(snap.stat().st_mode & 0o777, 0o700)
        (self.home / 'dirlink').symlink_to(ROOT, target_is_directory=True)
        with self.assertRaises(ValueError):
            backup.snapshot(self.home, ['dirlink/README.md'])
        with self.assertRaises(ValueError):
            backup.snapshot(self.home, ['../outside'])

    def test_backup_cli_uses_actual_managed_list(self):
        self.initialize()
        self.run_cm('apply', '--force')
        result = subprocess.run(['python3', str(ROOT / 'scripts/backup.py'), 'snapshot',
                                 '--source', str(ROOT), '--home', str(self.home)], env=self.env,
                                text=True, capture_output=True, check=True)
        snap = Path(result.stdout.strip().removeprefix('Snapshot: '))
        paths = {entry['path'] for entry in json.loads((snap / 'manifest.json').read_text())['files']}
        self.assertIn('.zshrc', paths)
        self.assertNotIn('.ssh/id_rsa', paths)

    def test_plan_has_no_side_effects_and_bad_profiles_fail(self):
        env = dict(self.env, DOTFILES_PROFILES='full')
        result = subprocess.run([str(ROOT / 'scripts/bootstrap')], env=env, text=True, capture_output=True, check=True)
        self.assertIn('mactex', result.stdout)
        self.assertIn('azure-cli', result.stdout)
        self.assertEqual(list(self.home.iterdir()), [])
        result = subprocess.run([str(ROOT / 'scripts/bootstrap'), '--profile', 'typo'], env=env, capture_output=True)
        self.assertNotEqual(result.returncode, 0)

    def test_shell_starts_with_no_optional_tools(self):
        self.initialize('linux')
        self.run_cm('apply', '--force')
        env = dict(self.env, PATH='/usr/bin:/bin', TERM='xterm-256color')
        command = 'source "$HOME/.zshenv"; source "$HOME/.zshrc"; print -r -- ready'
        result = subprocess.run(['zsh', '-dfic', command], env=env, text=True, capture_output=True, check=True)
        self.assertIn('ready', result.stdout)
        self.assertEqual(result.stderr, '')


if __name__ == '__main__':
    unittest.main()
