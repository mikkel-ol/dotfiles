function mzjs-host() {
    if [ -z "$1" ]; then
        echo "Usage: $0 <version>"
        exit 1
    fi

    VERSION=$1

    echo "Installing @mz-js/host-cli@$VERSION globally..."
    npx -y @mz-js/host-cli@$VERSION

    directories=(
        "private"
        "business"
        "advisory"
    )

    # Define process_directory script content
    process_script=$(mktemp)
    cat <<EOF >"$process_script"
#!/bin/bash
dir=\$1
version=\$2

cd "\$dir" || exit

echo "Processing directory \$dir"
git stash --include-untracked
git checkout master
git pull
git checkout -b "feat/mzjs-angular-\$version"

rm -rf node_modules package-lock.json
npx -y @mz-js/host-cli@\${version} update .
git checkout master package-lock.json
npm i

git add .
git commit -m "Bump Mozaic to \$version"
git push --set-upstream origin "feat/mzjs-angular-\$version"

echo "Creating pull request for \$dir..."
gh pr create --title "Bump Mozaic to \$version" --body "" --base master

echo "Pull request created for \$dir"
EOF
    chmod +x "$process_script"

    echo "Running updates"
    printf "%s\n" "${directories[@]}" | xargs -I {} -P 4 bash "$process_script" "{}" "$VERSION"

    echo "Cleaning up"
    rm -f "$process_script"

    echo "Done"
}

function mzjs-sync() {
    npm run sync --prefix ~/.config/mzjs -- "$(pwd)"
}

function mzjs-mf-pr() {
    # Parse required arguments
    local FILE_TO_UPDATE=""
    local BRANCH_NAME=""
    local COMMIT_MESSAGE=""
    local DRY_RUN=false

    while [[ "$#" -gt 0 ]]; do
        case "$1" in
        --file)
            FILE_TO_UPDATE="$2"
            shift 2
            ;;
        --branch)
            BRANCH_NAME="$2"
            shift 2
            ;;
        --message)
            COMMIT_MESSAGE="$2"
            shift 2
            ;;
        --dry)
            DRY_RUN=true
            shift
            ;;
        *)
            echo "Unknown parameter: $1"
            return 1
            ;;
        esac
    done

    # Validate required arguments
    if [[ -z "$FILE_TO_UPDATE" || -z "$BRANCH_NAME" || -z "$COMMIT_MESSAGE" ]]; then
        echo "Usage: cat some-file | update_repos --file <file-path> --branch <branch-prefix> --message <commit-message> [--dry]"
        return 1
    fi

    # Read piped input into NEW_CONTENT
    if [ -t 0 ]; then
        echo "Error: No input detected. Pipe content into this function."
        return 1
    fi

    local NEW_CONTENT
    NEW_CONTENT=$(cat) # Read entire stdin into NEW_CONTENT

    # Function to determine the default branch (main or master)
    get_default_branch() {
        git remote show origin | awk '/HEAD branch/ {print $NF}'
    }

    # Function to process a repository
    process_repo() {
        local repo_dir="$1"
        local new_content="$2"

        # Ensure it's a git repository
        if [ ! -d "$repo_dir/.git" ]; then
            echo "Skipping $repo_dir (not a git repository)"
            return
        fi

        cd "$repo_dir" || return

        # Fetch latest changes
        git fetch origin

        # Determine the default branch
        local BASE_BRANCH
        BASE_BRANCH=$(get_default_branch)
        if [ -z "$BASE_BRANCH" ]; then
            echo "Skipping $repo_dir (unable to determine default branch)"
            cd ..
            return
        fi

        # Create a new branch
        git checkout -b "$BRANCH_NAME" origin/"$BASE_BRANCH"

        # Update file content
        echo "$new_content" >"$FILE_TO_UPDATE"

        # Commit changes
        git add "$FILE_TO_UPDATE"
        git commit -m "$COMMIT_MESSAGE"

        if [ "$DRY_RUN" = true ]; then
            echo "Dry run mode: Changes are committed locally in $repo_dir on branch $BRANCH_NAME"
            cd ..
            return
        fi

        # Push branch
        git push origin "$BRANCH_NAME"

        # Create pull request
        gh pr create --base "$BASE_BRANCH" --head "$BRANCH_NAME" --title "$COMMIT_MESSAGE" --body ""

        # Go back to parent directory
        cd ..

        echo "PR created for $repo_dir"
    }

    # Iterate over all directories in the current folder and process repositories
    local processed_count=0
    for dir in */; do
        process_repo "${dir%/}" "$NEW_CONTENT"
        ((processed_count++))

        if [ "$DRY_RUN" = true ]; then
            echo "Dry run mode: Only processing first repository."
            break
        fi
    done

    echo "All repositories processed."
}
