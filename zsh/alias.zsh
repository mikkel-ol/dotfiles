# Neovim
alias n="nvim"
alias v="nvim"

# Zsh
alias szsh="source ~/.zshrc"
alias vzsh="vim ~/.zshrc"
alias vzsha="vim ~/.zsh-alias"
alias szsh='source ~/.zshrc'

# IP
alias myip='dig +short myip.opendns.com @resolver1.opendns.com'

# MS SQL
alias sql='docker start sql'
alias sqlstop='docker stop sql'

# TCP Dump
alias tcp='sudo tcpdump'

# MySQL
alias startmysql='brew services start mysql'
alias stopmysql='brew services stop mysql'

# Hollywood
alias hollywood='docker run -it jess/hollywood'

# AWS mikkel.website
alias sshaws='ssh -i /Users/mikkel/Google\ Drive/aws/ikkel.dk.pem -R 52698:localhost:52698 ubuntu@ikkel.dk'

# VSCode current folder
alias code.='code .'
alias c='code .'

# Angular
alias ngs='ng serve'

# Python web server
alias pweb='python3 -m http.server'

# Git
alias git=hub
alias gbsel='git branch-select'
function add() {
  if [ "$1" != "" ]; then
    git add "$1"
  else
    git add .
  fi
}
function commit() {
  if [ "$1" != "" ]; then
    git commit -m "$1"
  else
    git commit -m Update
  fi
}
function gitall() {
  git add .
  if [ "$1" != "" ]; then
    git commit -m "$1"
  else
    git commit -m Update
  fi
  git pull
  git push
}
function gnb() {
  git checkout -b "$1"
  git push -u origin "$1"
}
function gchgb() {
  if [ $# -eq 0 ]; then
    echo "You must specify a branch"
    return -1
  fi
  git stash -u
  if is_in_local "$1"; then
    git checkout "$1"
  else
    gnb "$1"
  fi
  git stash pop
}

greset() {
  git switch main --discard-changes
  git reset --hard
  git clean -fd
}

# Local:
# https://stackoverflow.com/questions/21151178/shell-script-to-check-if-specified-git-branch-exists
# test if the branch is in the local repository.
# return 1 if the branch exists in the local, or 0 if not.
function is_in_local() {
  local branch=${1}
  local existed_in_local=$(git branch --list ${branch})

  if [[ -z ${existed_in_local} ]]; then
    return 1
  else
    return 0
  fi
}

# .NET
function dotrun() {
  dotnet watch -p "$1" run
}

alias db='dotnet build'

# IDF
alias get_idf='. $HOME/esp/esp-idf/export.sh'

# Mouse acceleration
alias macc_off='defaults write .GlobalPreferences com.apple.mouse.scaling -1'
alias macc_on='defaults write .GlobalPreferences com.apple.mouse.scaling 1'

# Random
function random() {
  local character_count=${1:-32}
  local character_set='A-Za-z0-9!?#-_'
  head /dev/urandom | LC_ALL=C tr -dc ${character_set} | fold -w ${character_count} | head -1
}

# Python
alias pip=pip3
alias python=python3

# Weather
alias weather='curl wttr.in/Aarhus'

# Recursively create .gitkeep files in all empty directories
alias gkeep='find . -type d -empty -not -path "./.git/*" -exec touch {}/.gitkeep \;'

# Git sync (requires hub)
alias gs='git sync'

# Cisco VPN name servers
alias cisco='. ~/cisco'

# REPL
alias repl="NODE_PATH=$(npm root --location=global) node ~/git/dotfiles/.repl.js"

# RxJS Docs
function rxdoc() {
  open https://rxjs.dev/api/operators/"$1"
}