Python Interactive Search and Select Tool (pySearchSelect)
==============

pySearchSelect is an interactive search and select line selection tool for
ASCII, operating via a full-screen Curses-based terminal session. It is
primarily written to be used by other scripts (like bash, python, perl) to make
useful scripts.

Software requirement:

This python script requires urwid (one of the python curses library). On ubuntu
you can install urwid by executing "sudo apt-get install  python-urwid" In case
you do not have install permission, you can just download urwid tar from
http://excess.org/urwid/ and untar the tar.gz at some place and add this
script(pySearchSelect) to the same directory.

Key Bindings:
```
Search box key bindings:
enter, tab, down, up, esc : move to the first element in the list

List key bindings:
enter      : exits after writing the selection to the given file.
q          : exits without writing the selection to the given file.
Up         : Move up
Down       : Move down
Left Mouse : selects an item.
```
Usage:
````
usage: pySearchSelect [-h] -f FILE -l [line [line ...]]

Interactive search and selection of ASCII lines using python

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File to write the user selection.
  -l [line [line ...]], --lines [line [line ...]]
                        Lines to be displayed interactively to the user
  -l [line [line ...]], --lines [line [line ...]]
```
Examples:

Simple Usage:

This command will open full screen Curses-based terminal session. And then
depending on the user selection, the user selection will be written to the file
specified in -f argument of the command.

pySearchSelect -f ~/.result -l line1 line2 line3

Advanced Usage:

pySearchSelect is useful when you create wrappers over it. I was using it to
interactively select my clearcase views using the myviews function given below
in my .bashrc

```bash
function myviews()
{
    resultFile=~/.selectedview
    # clear any previous selection.
    cat /dev/null > $resultFile
    allViews=$(cleartool lsview -short | grep $LOGNAME)
    # pySearchSelect shall be in your $PATH
    pySearchSelect -f $resultFile -l $allViews
    # if file has some contents
    if [[ -s $resultFile ]]; then
        cleartool setview $(cat $resultFile)
    fi
}
```
TODO: 
- [ ] Implement quick select
