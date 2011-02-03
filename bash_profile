# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin

export PATH

# General
alias grep='grep --color=auto'
alias l.='ls -d .* --color=auto'
alias ll='ls -l --color=auto'
alias ls='ls --color=auto'
alias mingw32-env='eval `rpm --eval %{_mingw32_env}`'
alias sprunge='curl -F '\''sprunge=<-'\'' http://sprunge.us'
alias vi='vim'

# Custom stuff
alias sprunge="curl -F 'sprunge=<-' http://sprunge.us"
