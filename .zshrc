export ZSH="$HOME/.oh-my-zsh"
export NVM_LAZY_LOAD="true"

DEFAULT_USER=`whoami`

ZSH_THEME="agnoster-timestamp-newline"

plugins=(
	git
	zsh-nvm
)

source $ZSH/oh-my-zsh.sh

#source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
source /home/mikkel/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

export NVM_DIR="$HOME/.nvm"
#[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
#[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

source ~/git/dotfiles/.zsh-alias

#eval "$(/bin/brew shellenv)"
#eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

export CHROME_BIN='/mnt/c/Program Files/Google/Chrome/Application/chrome.exe'

# Load Angular CLI autocompletion.
source <(ng completion script)
