"----- General program stuff -----

" Add vundle to our include path
set rtp+=~/.vim/bundle/vundle/

" Call vundle
call vundle#rc()

" Stop vim from pretending its vi
set nocompatible

" Support all newline styles
set fileformats=unix,dos,mac

" Make viminfo store our cursor location
set viminfo='10,\"100,:20,%,n~/.viminfo

" Command line history length
set history=1000

" Automagically re-read the file if it gets edited outside of vim
set autoread

" Enable modelines
set modeline

" Check 4 modelines for set commands
set modelines=4

"----- GUI display stuff -----
if has("gui_running")
	" Remove the toolbar
	set guioptions-=T
endif

"----- Display stuff -----

" Allways show the status line
set laststatus=2

" Custom status line
set statusline=%F%m%r%h%w\ (%{&ff}){%Y}\ [%l,%v][%p%%]

" Display a warning if the fileformat is not unix
set statusline+=%#warningmsg#
set statusline+=%{&ff!='unix'?'['.&ff.']':''}
set statusline+=%*

" Display a warning if the file encoding is not utf-8
set statusline+=%#warningmsg#
set statusline+=%{(&fenc!='utf-8'&&&fenc!='')?'['.&fenc.']':''}
set statusline+=%*

" Display a warning if we have mixed indentation or trailing whitespace
set statusline+=%#error#
set statusline+=%{StatuslineTabWarning()}
set statusline+=%*

set statusline+=%{StatuslineTrailingSpaceWarning()}

" Display syntax errors if we can
if exists("SyntasticStatuslineFlag")
	set statusline+=%#warningmsg#
	set statusline+=%{SyntasticStatuslineFlag()}
	set statusline+=%*
endif

" Enable line numbers
set number

" Show the current position
set ruler

" Hilight the screen line
set cursorline

" Set the window title to the filename/title string
set title

" Show matching braces
set showmatch

" GUI font
set guifont=Courier_New\ 8

" Enable detection of filetype
filetype plugin indent on

" Enable syntax hilighting
syntax on

" Tell vim we have a light background
set bg=light

" Tab completion stuff
set wildmenu
set wildmode=list:longest,full

" Disable making a backup before overwriting a file
set nobackup
set nowritebackup

" Show command output
set showcmd

"----- Editing/search stuff -----

" Enable mouse support
set mouse=a

" Hilight serach results
set hlsearch

"" Indentation stuff

" Enable auto indentation
set autoindent

" Backstop behaviour
set bs=2

" Who wants a 8 tab stop, use 4!
set tabstop=4

"" Encoding stuff

" We use utf-8 encoding
set enc=utf-8
set fileencodings=utf-8

"" Line wrapping stuff

" Break the line at the breakat
set linebreak

" Automagically wrap lines at 80
set textwidth=80

" Enable spell checking
set spl=en spell

"----- Vundle bundle stuff -----
Bundle 'gmarik/vundle'
Bundle 'fugitive.vim'
Bundle 'Markdown'
Bundle 'Markdown-syntax'
Bundle 'taglist.vim'

"----- Tag list stuff -----

" Make the taglist appear on the right
let Tlist_Use_Right_Window = 1

" Make the taglist fold the column
let Tlist_Enable_Fold_Column = 0

" Make vim exit if only the taglist is open
let Tlist_Exit_OnlyWindow = 1

" Jump to a tag when single clicked on
let Tlist_Use_SingleClick = 1

" Taglist width
let Tlist_Inc_Winwidth = 0

"----- Auto run commands -----

" After writing the file if the file matches any regex then make it executable
autocmd BufWritePost *.sh,*.pl,*.py silent!chmod u+x %

" If this is a new file then automagically go into insert mode
autocmd BufNewFile * startinsert

" Remove any trailing whitespace
autocmd BufRead,BufWrite * silent! %s/\s\+$//ge

" Recalculate b:statusline_tab_warning when idle and on write
autocmd cursorhold,bufwritepost * unlet! b:statusline_tab_warning

" Recalculate b:statusline_long_line_warning when idle or on write
autocmd cursorhold,bufwritepost * unlet! b:statusline_long_line_warning

"----- Functions -----

" Check if we have trailing whitespace and if we do return the warning text
function! StatuslineTrailingSpaceWarning()
	if !exists("b:statusline_trailing_space_warning")
		if search('\s\+$', 'nw') != 0
			let b:statusline_trailing_space_warning = '[\s]'
		else
			let b:statusline_trailing_space_warning = ''
		endif
	endif
	return b:statusline_trailing_space_warning
endfunction

" Check if we have mixed tabs and spaces
function! StatuslineTabWarning()
	if !exists("b:statusline_tab_warning")
		let tabs = search('^\t', 'nw') != 0
		let spaces = search('^ ', 'nw') != 0

		if tabs && spaces
			let b:statusline_tab_warning = '[mixed-indenting]'
		elseif (spaces && !&et) || (tabs && &et)
			let b:statusline_tab_warning = '[&et]'
		else
			let b:statusline_tab_warning = ''
		endif
	endif
	return b:statusline_tab_warning
endfunction

"----- Key mappings -----

" Map F2 in normal modes to my signoff line
nmap <F2> <ESC>o<CR>Signed-off-by: Damian Zaremba <damian@damianzaremba.co.uk><ESC>

" Map F2 in insert modes to my signoff line"
imap <F2> <CR>Signed-off-by: Damian Zaremba <damian@damianzaremba.co.uk>

" Map F12 in all modes to enabling the taglist
nnoremap <F12> :TlistToggle
