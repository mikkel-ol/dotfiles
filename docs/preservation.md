# Preservation correction — 2026-09-14

The initial implementation exceeded the requested scope by changing shell, Git and editor preferences. Those changes were corrected after the user clarified that only installation, application and loading may change.

## Recovered and restored

| Area | Restored behavior |
| --- | --- |
| zsh environment | Original `ZSH` and `NVM_LAZY_LOAD`; remove invented global XDG/PATH/history/editor defaults |
| Prompt and plugins | Oh My Zsh, exact `laksnoster` theme, original five plugins; no Starship, zoxide or native-vi replacement |
| Aliases/widgets | Original module files and commands, including `git=hub`, original fzf execution widgets and project helpers |
| Runtime loading | fnm with original final activation flags, chruby loading, original Bun/pnpm paths; no mise activation |
| Git | Original default identity and personal conditional include under `~/dev/mikkel-ol/`; remove added Git policy settings |
| Neovim | Original lazy.lua (1,758 bytes), update checker, lazy bootstrap and bufferline spec; no unsolicited keymap repairs |
| Kitty | Original active settings, including original Cmd+10 binding; do not repair keybindings as part of migration |
| VS Code | Restore database settings and original agent URL/terminal approval preferences removed by the initial import |
| SSH seed | Original host aliases; remove additional SSH connection options |
| OpenCode | Remove invented generic seed; private original configuration remains unmanaged |
| Installation | Keep original managers and clients; no forced tldr replacement or automatic unlinking |

The corrected shell, Git, Neovim, Kitty and VS Code files were applied to the live machine after private snapshots were created. Other applications were not relaunched and no package replacement was performed during the correction. Old generated Starship/mise/combined-alias files may remain on disk, but the restored shell no longer loads them and the repository no longer manages them.

## Permitted loading changes

Home-directory paths use `$HOME`; Homebrew paths are detected for the platform. Stale shell wrapper files that pointed at a missing checkout are replaced with the original module contents from this repository. The RxJS helper is deployed to a stable configuration path. Optional sources are checked before loading, unmatched globs are tolerated, and duplicate fnm initialization is reduced to the original final activation call. None of these changes redesigns the original commands or preferences.

## Recovery limitation

The original `~/.config/git/ignore` was overwritten by the first generated configuration. No pre-apply backup was present, and `git log --all` contains no version of that path. Its original contents cannot be reconstructed reliably. The current file has been privately backed up and is now unmanaged; no original content has been guessed. The repository's root `.gitignore` is a different file and is not a substitute.

The original Kitty file's long default-comment text was not captured in full; the active preference lines were captured and have been restored. VS Code settings were captured and restored as values; JSON formatting/order may differ. The live original theme and shell module files were available, and Neovim's changed files were recoverable from the initial captured content.

## Protection going forward

Every full chezmoi apply now snapshots existing managed files before writes. The test suite checks original shell preferences, Git identity routing, editor settings, automatic backups, repeat application and rollback in disposable homes. This prevents another configuration redesign from being mistaken for a loading-only migration.
