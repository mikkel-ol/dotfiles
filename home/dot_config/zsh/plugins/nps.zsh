# FZF npm script picker for package.json
npm-scripts-widget() {
  # Walk up from current directory to find nearest package.json
  local dir=$PWD
  while [[ $dir != / && ! -f "$dir/package.json" ]]; do
    dir=${dir:h}
  done

  # If no package.json found, return
  if [[ ! -f "$dir/package.json" ]]; then
    return 1
  fi

  # Use jq to extract scripts from package.json
  local scripts=$(jq -r '.scripts // {} | to_entries[] | "\(.key)\t\(.value)"' "$dir/package.json") || return 1

  if [[ -z "$scripts" ]]; then
    return 1
  fi

  # Use fzf to pick a script
  local selection=$(echo "$scripts" | fzf \
    --height='-40%' \
    --min-height='20+' \
    --bind='ctrl-z:ignore' \
    --with-nth=1 \
    --accept-nth=1 \
    --delimiter='\t' \
    --preview='echo {2} | bat --language=sh --color=always --style=plain' \
    --preview-window=down)

  if [[ -z "$selection" ]]; then
    return 0
  fi

  # Set the command to run and run it
  BUFFER="npm run $selection"
  zle accept-line
}

zle -N npm-scripts-widget
bindkey "®" npm-scripts-widget
