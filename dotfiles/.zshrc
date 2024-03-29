# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"
export PATH="/opt/homebrew/bin:$PATH"
export PATH="/usr/local/bin:$PATH"

# Update reminder settings
zstyle ':omz:update' mode reminder
zstyle ':omz:update' frequency 13

plugins=(
    colored-man-pages # https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/colored-man-pages
    colorize # https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/colorize
    zoxide # https://github.com/ajeetdsouza/zoxide
    zsh-syntax-highlighting # https://github.com/zsh-users/zsh-syntax-highlighting
    zsh-autosuggestions # https://github.com/zsh-users/zsh-autosuggestions
    zsh-fzf-history-search # https://github.com/joshskidmore/zsh-fzf-history-search
)

# https://github.com/zsh-users/zsh-completions
fpath+=${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions/src

source $ZSH/oh-my-zsh.sh

# Generated for envman. Do not edit.
[ -s "$HOME/.config/envman/load.sh" ] && source "$HOME/.config/envman/load.sh"

# https://starship.rs/
eval "$(starship init zsh)"

alias l='ls -al'
alias c='clear'
alias grep='grep --color=auto'
alias g='git'
alias k='kubectl'
alias t='terraform'
alias tg='terragrunt'

alias clip='xclip -selection clipboard'
alias clipi='xclip -selection clipboard -i'

if [[ -f ~/.zshrc-tmp ]]; then
    source ~/.zshrc-tmp
fi

function reload() {
    source ~/.zshrc
    echo 'Config reloaded'
}

# ansible autocompletion
# eval "$(register-python-argcomplete ansible)"
# eval "$(register-python-argcomplete ansible-playbook)"

# >>>> Vagrant command completion (start)
fpath=(/opt/vagrant/embedded/gems/2.2.19/gems/vagrant-2.2.19/contrib/zsh $fpath)
compinit
# <<<<  Vagrant command completion (end)

autoload -U +X bashcompinit && bashcompinit

export PATH=$PATH:/usr/local/go/bin

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

if [ -e /home/jakub/.nix-profile/etc/profile.d/nix.sh ]; then . /home/jakub/.nix-profile/etc/profile.d/nix.sh; fi # added by Nix installer

# Disable auto cd
unsetopt autocd

readonly AWS_COMPLETER_BIN_PATH=$(which aws_completer)

complete -o nospace -C /usr/local/bin/terraform terraform
complete -C $AWS_COMPLETER_BIN_PATH aws

source <(kubectl completion zsh)

. "$HOME/.asdf/asdf.sh"

export AWS_DEFAULT_REGION="eu-central-1"

export HISTFILESIZE=999999999
export HISTSIZE=999999999
export HISTCONTROL=ignoredups
export SAVEHIST=$HISTSIZE

eval "$(logcli --completion-script-zsh)"

export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
