# Weather
alias weather='curl wttr.in/Aarhus'

# RNG
function random() {
    local character_count=${1:-32}
    local character_set='A-Za-z0-9!?#-_'
    head /dev/urandom | LC_ALL=C tr -dc ${character_set} | fold -w ${character_count} | head -1
}

# Hollywood
alias hollywood='docker run -it jess/hollywood'

# IP
alias myip='dig +short myip.opendns.com @resolver1.opendns.com'

# TCP Dump
alias tcp='sudo tcpdump'
