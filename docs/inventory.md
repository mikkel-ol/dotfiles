# Configuration inventory — 2026-09-14

Scope: home-directory configuration names, `~/.config`, selected application preferences, Homebrew packages, runtime versions, VS Code extensions, fonts and an allowlist of macOS preferences. This is a configuration audit, not a full disk/credential backup. The controlling rule is to preserve existing preferences and change only installation, application and loading.

## Managed configuration

| Original | Repository treatment |
| --- | --- |
| zsh startup files | Original settings and plugin order; portable source/PATH loading |
| `~/.config/zsh/{alias,config,plugins}` | Original module contents; obsolete wrappers resolved to repository originals |
| `~/.oh-my-zsh/custom/themes/laksnoster.zsh-theme` | Exact custom theme, versioned directly |
| Oh My Zsh and third-party plugins | Original installed revisions in `packages/shell-plugins.json`; install missing dependencies only |
| Git user settings | Original default/personal identities and include directory; `gh` resolved through PATH |
| `~/.gitconfig-personal` | Same identity override, with values in local chezmoi data |
| `~/.config/git/ignore` | Unmanaged: original contents were not recoverable; see preservation audit |
| `~/.config/nvim` | Captured LazyVim config, lockfile, keymaps, extras and formatter settings; preferences preserved |
| `~/.config/kitty` | Original active settings and exact selected theme; downloaded theme collection omitted |
| AeroSpace | Original layouts, gaps, keybindings and monitor preferences |
| Karabiner | Original Caps Lock→Escape, F13 shortcut and ISO keyboard preference |
| VS Code | All captured preference values and keybindings, plus 36 extension IDs |
| Zed | Original UI/theme/font/Vim/telemetry settings |
| Sublime Text | Original user font/indexing/ignored-package settings |
| GitHub CLI | Portable `config.yml`; authentication excluded |
| Docker | Original `daemon.json`; account/context state excluded |
| SSH | Original host-alias seed for a new machine; existing file and keys preserved |
| Codex/Claude | Existing user instructions, personal skills and initial preferences; app-managed existing settings preserved |
| OpenCode | Private provider configuration remains unmanaged; no replacement preferences imposed |
| Public agent skills | Source manifest and optional installer; upstream contents are not pinned |
| macOS | Seven original preference values in `macos/defaults.json`; explicit opt-in |
| Fonts | Fira Code and Nerd Font casks; licensed/custom fonts restored separately |

Fish's config, Lazygit's config and Zed's keymap were empty/default and had no custom payload to import. iTerm2 contained an application-support pointer rather than a preference payload. Unused Neovim example documentation, theme catalogs, auto-backups and app runtime state are omitted.

## Tool installation

Homebrew group files declare the observed core, desktop, AI, work, creative and specialist tools. fnm, chruby/ruby-install, `z`, hub and the installed tldr client are retained. `packages/runtimes.json` records the captured versions for missing installations through the existing managers. Existing runtime defaults and package installations are not reset.

The deprecated `codex-app` cask is excluded because Homebrew marked it discontinued; use the supported desktop distribution. No existing app is removed. GUI app conflicts must be resolved individually without automatic deletion.

## Private/manual handoff

| Category | New-machine action |
| --- | --- |
| SSH keys and agent | Generate or securely transfer keys and register them with Git hosting; adjust original key filenames locally if needed |
| npm/NuGet registries | Restore routing locally and authenticate; tokens and private feed configuration are not committed |
| Azure, Kubernetes, VPN, Android signing, development certificates | Authenticate and restore approved credentials/certificates through their normal tools |
| Docker authentication/contexts | Sign in and recreate contexts; only daemon preferences are portable |
| GitHub CLI | `gh auth login`; `hosts.yml` is not committed |
| AI tools, private providers, plugin connections, MCP servers, automations | Sign in and restore machine/account-specific configuration separately |
| Private work skills/helpers and linked Node packages | Restore from the owning private repository after authentication |
| Editor database connections, account sync and workspaces | Reconnect; workspace/session databases are excluded |
| Custom/purchased fonts | Restore licensed originals |
| Xcode and Apple Developer app | Install through Apple, accept licenses and install required SDKs |
| Adobe apps | Install through Creative Cloud with the appropriate license |
| Office/Teams/OneDrive | Packages in work profile; account/license activation remains manual |
| Corporate security, enrollment, VPN, printing and admin tools | Use employer-managed installers; do not copy organizational policies or privileged agents |
| AeroSpace, Karabiner, Docker, Homerow, Logitech tools | Complete first-launch permissions and activation; original preferences are preserved |
| Wallpaper override launch agent | Machine/organization-specific; left local |

Histories, caches, process locks, databases, browser profiles, conversations, Keychain data, cloud credentials, package tokens, downloaded dependencies and generated vendor agents are excluded. macOS supplies Safari and other system apps.

See [the preservation audit](preservation.md) for exactly what was recovered after the initial implementation, and [validation](validation.md) for the tested scope.
