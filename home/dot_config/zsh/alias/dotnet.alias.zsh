alias db='dotnet build'

function dotrun() {
    dotnet watch -p "$1" run
}
