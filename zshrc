# oh-my-zsh
DEFAULT_USER=$(whoami)
ZSH_THEME="agnoster"

source $ZSH/oh-my-zsh.sh

plugins=(
    git
    macos
    docker
    dotnet
    kubectl
)

# zsh auto suggestions
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh

# fzf
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# zsh syntax highlighting
source $HOME/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# configs
for f ($HOME/.config/zsh/config/*.zsh) . $f

# alias
for f ($HOME/.config/zsh/alias/*.zsh) . $f

source $ZSH/oh-my-zsh.sh
