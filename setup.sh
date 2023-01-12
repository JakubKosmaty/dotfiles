#!/usr/bin/env bash

set -euo pipefail

readonly SSH_KEY_PATH="${HOME}/.ssh/id_ed25519"

is_command_exists() {
  command -v $1 &> /dev/null
}

is_dir_exists() {
  [ -d $1 ]
}

is_file_exists() {
  [ -f $1 ]
}

apt_upgrade() {
  echo "Upgrading installed packages"
  sudo apt update
  sudo apt upgrade
}

install_curl() {
  echo "Installing curl"
  sudo apt install -y curl
}

install_git() {
  echo "Installing git"
  sudo apt install -y git
}

install_nixos() {
  echo "Installing NixOS"
  sh <(curl -L https://nixos.org/nix/install) --daemon
}

install_devbox() {
  echo "Installing Devbox"
  curl -fsSL https://get.jetpack.io/devbox | bash
}

clone_dotfiles() {
  git clone git@github.com:JakubKosmaty/dotfiles.git
}

generate_ssh_key() {
  ssh-keygen -t ed25519 -C "jacobkosmaty@gmail.com" -f $SSH_KEY_PATH
  cat "${SSH_KEY_PATH}.pub"
  echo "Add SSH Key to https://github.com/settings/keys"
  read -p "Press enter to continue"
}

main() {
  apt_upgrade
  ! is_command_exists "curl" && install_curl
  ! is_command_exists "git" && install_git
  ! is_command_exists "nix" && install_nixos
  ! is_command_exists "devbox" && install_devbox
  ! is_file_exists $SSH_KEY_PATH && generate_ssh_key
  ! is_dir_exists "dotfiles" && clone_dotfiles
}

main
