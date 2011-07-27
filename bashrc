if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Fix my $PATH
export PATH="/home/damian/Komodo-IDE-6/bin:$PATH"
export PATH="/usr/local/ruby/bin/:$PATH"
export PATH="/home/damian/go/bin/:$PATH"
export PATH="/usr/local/arcanist/bin/:$PATH"
export PATH="/usr/local/appengine/:$PATH"

# Make somethings prettier with alises
alias grep='grep --color=auto'
alias l.='ls -d .* --color=auto'
alias ll='ls -l --color=auto'
alias ls='ls --color=auto'
alias mingw32-env='eval `rpm --eval %{_mingw32_env}`'
alias vi='vim'

# Useful alises
alias sprunge="curl -F 'sprunge=<-' http://sprunge.us"
