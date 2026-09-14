# Validation record — preservation correction, 2026-09-14

Completed on the source Apple Silicon Mac:

- Nine tests passed in disposable homes: file rendering/convergence, Linux selection, original identity rules, preserved shell/editor preferences, existing private files, automatic pre-apply backups, rollback and preview safety.
- ShellCheck, shfmt and per-file zsh syntax checks passed. Gitleaks found no secrets in the working tree. Documentation links and `git diff --check` passed.
- A real interactive login shell in a pseudo-terminal loaded `laksnoster`, the original five Oh My Zsh plugins, `git=hub`, and the original Ctrl-G branch widget. fnm supplied Node. The shell exited successfully; no startup errors appeared in the interactive terminal.
- The restored Neovim `lazy.lua` matches the original captured size/content (1,758 bytes). The original automatic checker and bufferline spec were restored. No further headless plugin updates were run during correction.
- Corrected shell, Git, Neovim, Kitty and VS Code files were applied to the live machine after private snapshots were created. The exact recovery scope and limitations are in [preservation.md](preservation.md).

The initial implementation's eight-test result and headless Neovim smoke check predated the user's preservation correction; they are not evidence that the earlier preference changes were acceptable. The revised tests now assert preservation explicitly.

The previous implementation installed validation tools (including mise). The corrected shell does not activate mise, and the installer no longer provisions it. Existing unused installations are not uninstalled automatically.

No full workstation package reinstall was run during correction. New shell/runtime installer scripts were syntax-checked and their upstream command options were inspected; full installation on a fresh Mac and remote CI remain untested. The unrecoverable global Git ignore contents are documented rather than guessed.
