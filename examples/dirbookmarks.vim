" VIM is based on curses and so works great with curses applications.
" This little command shall be able to open the cdargs file.
function! Cd()
python << PYEND
    import sys
    sys.path.append('/home/jay/bin')
    import marks
    showBookmarks()
    let mydir = system("cat /home/raleigh/jrajpu10/.cdargsresult")
    " See http://stackoverflow.com/questions/4596932/vim-cd-to-path-stored-in-variable
    "cd `=mydir`
    edit `=mydir`
PYEND
endfunction
