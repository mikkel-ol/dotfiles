createGitHubRepo() {
    read -q "REPLY?Are you sure you want to share this publicly? "
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        local sourcePath=$(pwd)
        rsync -r --exclude=.git --exclude=node_modules . ~/dev/playground/shared/$1
        cd ~/dev/playground/shared/$1

        git init
        git add .
        git commit -m 'initial commit'
        gh repo create $1 --public --push --source=. --remote=upstream

        read -q "REPLY?Do you also want to create a StackBlitz? "
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            explorer.exe "https://stackblitz.com/github/mikkel-ol/$1"
        else
            gh repo view -w
        fi

        echo "Copy created at $(pwd), remaining in original directory"
        cd $sourcePath
    fi
}

share() {
    if [ -z "$1" ]; then
        read "NAME?What would you like to call this repo? "
        echo
        createGitHubRepo "$NAME"
    else
        createGitHubRepo "$1"
    fi
}
