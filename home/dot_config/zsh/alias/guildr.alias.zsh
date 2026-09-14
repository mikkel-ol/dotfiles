alias guildr-app='docker compose --env-file .env.prod build --no-cache app'
alias guildr-api='docker compose --env-file .env.prod build --no-cache api' 
alias guildr-app-push='docker push mikkelol/guildr-app:latest'
alias guildr-api-push='docker push mikkelol/guildr-api:latest'

alias guildr-app-dev='docker compose --env-file .env.dev build --no-cache app' 
alias guildr-api-dev='docker compose --env-file .env.dev build --no-cache api' 
alias guildr-app-dev-push='docker push mikkelol/guildr-app:beta'
alias guildr-api-dev-push='docker push mikkelol/guildr-api:beta'

alias guildr='guildr-app && guildr-api' 
alias guildr-dev='guildr-app-dev && guildr-api-dev'

alias guildr-push='guildr && guildr-app-push && guildr-api-push'
alias guildr-dev-push='guildr-dev && guildr-app-dev-push && guildr-api-dev-push'

