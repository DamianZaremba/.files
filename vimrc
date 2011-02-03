autocmd BufWritePost *.sh,*.pl,*.py if FileExecutable("%:p") | :!chmod a+x % ^@ endif
autocmd BufNewFile * startinsert

set number
set autoindent
filetype plugin on
filetype on
filetype indent on
tab all
set bs=2
set guifont=monospace\ 8
set history=1000
syntax on
set bg=dark
set tabstop=4
set autoread
set tabstop=4
set nocompatible
set ruler
set enc=utf-8
set fileencodings=utf-8,latin2
set hlsearch
set linebreak
set showmatch
set matchtime=2
set modeline
set modelines=4
set wildmenu
set showcmd
set nobackup
set nowritebackup
set textwidth=120
set cursorline
set title

nmap <F2> <ESC>o<CR>Signed-off-by: Damian Zaremba <damian@damianzaremba.co.uk><ESC> 
imap <F2> <CR>Signed-off-by: Damian Zaremba <damian@damianzaremba.co.uk>

if (&term == 'xterm')
        set t_Co=256
endif

function! FileExecutable (fname)
      execute "silent! ! test -x" a:fname
      return v:shell_error
endfunction
