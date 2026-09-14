alias git=hub
alias gbsel='git branch-select'
alias gkeep='find . -type d -empty -not -path "./.git/*" -exec touch {}/.gitkeep \;'
alias gs='git sync'

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
