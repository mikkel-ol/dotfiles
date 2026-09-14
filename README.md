# dotfiles

Your existing configuration, applied with **chezmoi** and installed with **Homebrew Bundle**.
The configuration is preserved: Oh My Zsh, your `laksnoster` theme, plugins, aliases, widgets, fnm, chruby, `z`, Git identities, and editor preferences. Changes are limited to installation, loading, and portable filesystem paths.

## New Mac

Install Apple's Command Line Tools (`xcode-select --install`), then:

```sh
git clone https://github.com/mikkel-ol/dotfiles.git ~/dotfiles
cd ~/dotfiles
./scripts/bootstrap --profile full          # preview; no changes
./scripts/bootstrap --apply --profile full  # install and apply
```

The default package selection is `desktop,ai`; `full` includes work, creative and specialist tools, including MacTeX. Homebrew may request administrator access. No submodule initialization is needed.

Bootstrap installs missing packages and original shell dependencies, initializes chezmoi, backs up existing files, applies configuration and installs missing runtimes/extensions. It keeps existing shell plugin checkouts, runtime defaults and installed global Node packages. It does not switch runtime managers, unlink existing tools, uninstall apps or rewrite preferences to a different style.

## Preview the existing checkout

Run once from this repository before using plain chezmoi commands:

```sh
chezmoi --source "$PWD" init --recurse-submodules=false
chezmoi diff
```

Initialization writes only chezmoi's local configuration. It does not apply dotfiles. A missing `~/.local/share/chezmoi` error means this initialization has not happened; you do not need another clone.

## Apply and maintain

```sh
chezmoi diff                         # inspect the proposed changes
chezmoi apply                        # automatically back up, then apply
chezmoi edit ~/.zshrc                 # edit the managed source
chezmoi add ~/.config/kitty/kitty.conf # capture an intentional app-side edit
chezmoi verify --exclude=scripts      # compare managed files
./scripts/packages check             # inspect missing packages
./scripts/packages install           # install missing packages without upgrading
./scripts/packages upgrade           # explicitly upgrade selected packages
./scripts/extensions --check
./scripts/doctor
./scripts/test
```

The always-run script shown in a chezmoi diff only creates a backup. Package installation is explicit through bootstrap/maintenance scripts. Exclude scripts when verifying file convergence, because that backup script is intentionally due on every apply.

## Packages and runtimes

| Group | Includes |
| --- | --- |
| `core` | Git, hub, gh, Neovim, zsh, fnm, chruby/ruby-install, z, search tools and validation tools |
| `desktop` | Editors, Kitty, AeroSpace, Karabiner, browsers, Docker Desktop, fonts and desktop tools |
| `ai` | Codex CLI, ChatGPT, Claude/Claude Code, Copilot, OpenCode and llm |
| `work` | Azure, .NET, Kubernetes, Gradle, Android tools, Office, Teams, Edge and OneDrive |
| `creative` | Image tools, Inkscape and MacTeX |
| `extras` | QEMU, Zathura, mainframe tools, Moonlight, Rectangle and Logitech software |
| `full` | All groups |

`core` is always included. Combine groups with commas. Successful bootstrap saves the choice in `~/.config/dotfiles/profiles`. The root `Brewfile` describes the default set; `packages/Brewfile.*` supplies all groups. Profiles choose packages; they do not change configuration preferences.

`packages/shell-plugins.json` records the installed Oh My Zsh/plugin commits. `scripts/shell-plugins.py --apply` installs missing copies without running upstream shell-setup scripts or overwriting existing files. The custom theme is versioned directly.

`packages/runtimes.json` captures Node, Ruby, Bun, pnpm, Angular CLI and Corepack versions. `scripts/runtimes.py --apply` uses fnm, ruby-install and npm/Corepack; it does not use mise. It sets a Node default only if none exists and sets up pnpm only for a newly installed Corepack. Python, Java/Gradle and .NET remain supplied by Homebrew/system tools. Neither existing project runtime files nor interactive Ruby selection is changed.

Homebrew and Marketplace extensions are rolling installations, not an OS snapshot. `tldr` is retained even though Homebrew marks it deprecated; the installer does not replace or unlink it. If an upstream package becomes unavailable, resolve that package explicitly.

## Preserved configuration

- zsh keeps the `laksnoster` theme and `git`, `git-open`, `macos`, `zsh-vi-mode`, `direnv` plugin list. Existing aliases and widgets keep their behavior, including their execution keybindings.
- Old wrapper paths pointing at a missing checkout are resolved into actual managed files. Home paths use `$HOME`, Homebrew paths use its detected prefix, and fnm is initialized once using the original final options.
- Git retains the default identity and the personal override under `~/dev/mikkel-ol/`. The credential helper is loaded through `gh` on PATH instead of a version-specific Cellar path. No new rebase, pruning, conflict, editor or signing policy is imposed.
- Neovim retains the captured LazyVim settings, automatic update checker, keymaps and lockfile. Kitty and VS Code retain the original preference values. Keybindings are not repaired or redesigned as part of dotfile migration.
- macOS defaults remain an explicit opt-in using the observed preference values.

Git names/addresses are stored in `~/.config/chezmoi/chezmoi.toml`. `email` is the personal address; `defaultEmail` is used elsewhere. Reconfigure with `chezmoi init --prompt`.

SSH, Codex and Claude initial settings use `create_` to preserve existing files. Credentials, private provider configuration, registry configuration, cloud logins, app sessions and private work skills remain outside Git. OpenCode's private settings are left unmanaged. Public skill sources can be reinstalled with `scripts/skills.py --apply`; personal Codex skills are captured.

See [the inventory](docs/inventory.md) and [the preservation audit](docs/preservation.md) for exact coverage and recovery limitations. In particular, the pre-apply global Git ignore file was not captured and cannot be reconstructed from repository history; it is now unmanaged.

## Backups and rollback

Every full `chezmoi apply` runs `home/run_before_00-backup.sh.tmpl`, which snapshots managed destinations before writes. Bootstrap additionally backs up the chezmoi configuration before initialization. Snapshots live under `~/.local/state/dotfiles/backups/` with a private parent directory and may contain private settings. Never add them to Git.

```sh
python3 scripts/backup.py restore /absolute/path/to/snapshot
```

Restore first saves current state, then restores original files/symlinks and removes files that did not exist at snapshot time. Installed packages and empty directories remain. Symlinked parent directories are rejected to avoid overwriting a different checkout through an old manager's links. `--exclude=scripts` bypasses automatic apply backups; use it only when deliberately managing backups yourself.

Stop using `rcup` after migration. The old root-level `config/`, `zshrc`, `zshenv`, `rcrc`, `hushlogin` and `repl/` remain preserved legacy material outside the managed `home/` source root. They are not deployed by the new installer; existing repository edits and the old Neovim submodule are retained.

## macOS and manual setup

```sh
./scripts/macos.py                    # preview only
./scripts/macos.py --apply            # back up and apply seven observed keys
./scripts/macos.py --restore /absolute/path/to/preferences-backup.json
```

App sign-ins, Accessibility/Input Monitoring, Xcode, licensed software and organization management require their normal interactive setup. Existing manually installed apps may conflict with Homebrew casks; resolve individual conflicts rather than deleting an app automatically. Details are in [the inventory](docs/inventory.md).

## Linux

The Linux scope is portable user configuration. Install Git, Python 3.11+, zsh, chezmoi and your desired tools through your distro, then:

```sh
./scripts/shell-plugins.py --apply
./scripts/bootstrap --apply --config-only
```

Mac-specific files under `Library/`, AeroSpace, Karabiner and Docker daemon settings are excluded. macOS-only aliases still describe macOS actions; they are preserved rather than rewritten. Linux GUI provisioning and Windows are outside scope.

## Validation

`./scripts/test` validates shell syntax, ShellCheck/shfmt, secret scanning and real chezmoi operations in disposable homes. Tests cover file convergence, platform selection, identity routing, preserved shell preferences, private-file preservation, automatic backups and rollback. GitHub Actions is configured for macOS and Ubuntu; no CI run or full fresh-Mac installation is implied by local tests.
