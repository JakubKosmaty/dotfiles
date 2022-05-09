# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

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

alias mc='/home/jakub/Documents/java8/amazon-corretto-8.332.08.1-linux-x64/bin/java -jar /home/jakub/Documents/java8/sklauncher.jar'
