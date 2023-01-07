# oh-my-zsh
DEFAULT_USER=$(whoami)
ZSH_THEME="agnoster"

source $ZSH/oh-my-zsh.sh

plugins=(
    git
    zsh-nvm
)

# zsh auto suggestions
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh

# fzf
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# zsh syntax highlighting
source $HOME/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# alias
for f (./.config/zsh/alias/*.zsh) . $f

# configs
for f (./.config/zsh/config/*.zsh) . $f