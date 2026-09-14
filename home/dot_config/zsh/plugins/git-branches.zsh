# ~/.config/zsh/plugins/git-branches.zsh

# Abort quietly if requirements are missing
if ! command -v fzf >/dev/null 2>&1; then
  return
fi
if ! command -v git >/dev/null 2>&1; then
  return
fi

git-fzf-branch() {
  if ! git rev-parse --git-dir >/dev/null 2>&1; then
    print -Pnr -- "%F{red}Not a git repository.%f" >&2
    return 2
  fi

  branch=$(git branch --all --color=never \
    | sed 's/^[* ]*//' \
    | sed 's#^remotes/##' \
    | sort -u \
    | fzf --height=40% --reverse --prompt='git branch> ' --border --inline-info) || return 1

  return 0
}


if [[ $- == *i* ]]; then
  git-fzf-branch-widget() {
    git-fzf-branch
    local ec=$?

    # Not a repo – already printed error, move to fresh prompt
    if (( ec == 2 )); then
      zle accept-line
      return
    fi

    # A branch was selected -> instead of executing, push `git checkout branch` into history
    if [[ -n $branch ]]; then
      BUFFER="git checkout $branch"   # place command at prompt
      CURSOR=${#BUFFER}
      zle accept-line                 # execute it + store in history
      return
    fi

    # Cancel (fzf quit) – just redraw
    zle -I
    zle redisplay
  }

  zle -N git-fzf-branch-widget
  bindkey -M emacs '^G' git-fzf-branch-widget 2>/dev/null
  bindkey -M viins '^G' git-fzf-branch-widget 2>/dev/null
fi