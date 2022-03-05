# oh-my-posh
Import-Module oh-my-posh
Set-PoshPrompt -Theme pure

# Terminal-Icons
Import-Module -Name Terminal-Icons

# PSReadLine
Set-PSReadLineKeyHandler -Chord 'Ctrl+d' -Function DeleteChar
Set-PSReadLineOption -PredictionSource 'History'
Set-PSReadLineOption -PredictionViewStyle 'ListView'
Set-PSReadLineOption -Colors @{ InlinePrediction = '#9CA3AF'}

# PSFzf
Import-Module PSFzf
Set-PsFzfOption -PSReadlineChordProvider 'Ctrl+f' -PSReadlineChordReverseHistory 'Ctrl+r'

# zoxide
Invoke-Expression (& {
    $hook = if ($PSVersionTable.PSVersion.Major -lt 6) { 'prompt' } else { 'pwd' }
    (zoxide init --hook $hook powershell | Out-String)
})

# env
$env:KUBE_EDITOR = "code -w"
$env:PATH += ";C:\Users\Jakub\Documents\JetBrainsScripts"
$env:JAVA_HOME = "C:\Users\Jakub\.jdks\temurin-11.0.13"
$env:PATH += ";$env:JAVA_HOME\bin"
$env:PYTHONIOENCODING="utf-8"

# Node.js version manager
fnm env --use-on-cd | Out-String | Invoke-Expression

# Alias
Set-Alias c clear
Set-Alias g git
Set-Alias k kubectl
Set-Alias v vagrant
function l {
  Get-ChildItem -Force @args
}
