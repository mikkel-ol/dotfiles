# Architecture: preserve configuration, modernize deployment

The user's clarified scope is authoritative: **do not redesign existing preferences or replace their tool choices; change only installation, application and loading**. The earlier recommendation to activate mise/Starship/zoxide was rejected and has been removed from the active source and installer.

## Ownership

- **chezmoi** deploys the existing configuration and parameterizes home paths and Git identity. `.chezmoiroot` keeps operational scripts and package declarations outside the deployed `home/` tree. [Source-root documentation](https://www.chezmoi.io/reference/special-files/chezmoiroot/)
- **Homebrew Bundle** installs the existing tool selection plus deployment/validation prerequisites. Installation uses `--no-upgrade`. No automatic cleanup or unlinking is performed. Homebrew is rolling release and has no supported Brewfile lockfile. [Homebrew Bundle](https://docs.brew.sh/Brew-Bundle-and-Brewfile)
- **Existing managers remain**: Oh My Zsh with the installed plugins and custom theme; fnm for Node; chruby/ruby-install for Ruby; Corepack/pnpm and Bun. New-machine versions are declared in `packages/runtimes.json`. Existing installations/defaults are retained.

## Deployment boundary

Portable path substitutions and fixing obsolete source locations are permitted. Changing prompt appearance, aliases, keybindings, editor settings, Git policy, permissions preferences or active runtime managers is not part of this migration. Tests enforce representative original preferences.

No credentials or app/session databases are imported. Private configurations that cannot be represented faithfully without credentials remain unmanaged instead of receiving an invented replacement. `create_` files seed compatible preferences only when absent; existing files are preserved. [chezmoi source attributes](https://www.chezmoi.io/reference/source-state-attributes/)

An always-run `run_before_` script snapshots managed destinations before each full apply, including plain `chezmoi apply`. It runs no package installers. Verification of file state uses `chezmoi verify --exclude=scripts`, since the backup script is intentionally always pending. [Script semantics](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/)

## Alternatives considered

Stow would preserve familiar files through symlinks, but would still require separate host-specific loading and installation conventions. Nix/Home Manager and mise can support broader declarative environments, but switching to them would exceed the clarified scope. These remain alternatives for a separate, explicit migration—not changes performed here. [GNU Stow](https://www.gnu.org/software/stow/), [nix-darwin](https://github.com/nix-darwin/nix-darwin), [mise](https://mise.jdx.dev/)

See [preservation and recovery](preservation.md) for the corrections made after the initial implementation and the one unrecoverable original file.
