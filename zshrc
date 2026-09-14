# oh-my-zsh
DEFAULT_USER=$(whoami)
ZSH_THEME="agnoster"

plugins=(
    git
    macos
    docker
    dotnet
    kubectl
)

# zsh auto suggestions
source $HOME/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh

# TODO: Keybinding not working
# fzf
[ -f $HOME/.fzf.zsh ] && source $HOME/.fzf.zsh

# zsh syntax highlighting
source $HOME/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# configs
for f ($HOME/.config/zsh/config/*.zsh) . $f

# alias
for f ($HOME/.config/zsh/alias/*.zsh) . $f

source $ZSH/oh-my-zsh.sh

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
