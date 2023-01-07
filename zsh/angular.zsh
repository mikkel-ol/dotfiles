alias play-angular="cd ~/dev/testing/angular && greset && code . && ng serve"
alias play-ionic="cd ~/dev/testing/ionic && git checkout -- . && code . && ionic serve"
alias play-nx="cd ~/dev/testing/nx && git checkout -- . && code ."

# Load Angular CLI autocompletion.
source <(ng completion script)
