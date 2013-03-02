Python Search Select (PSS)
==============

PSS is python module and script for interactive search and selection of ASCII
lines, operating via a full-screen curses-based terminal session.  It is
primarily written to be used by other scripts (like bash, python, perl) to make
useful scripts. PSS is acronym for "Python Search Select".

PSS shows a curses GUI which contains a list box and a search box(at the
bottom). First element in the list box is selected by default. You can change
the selection using mouse or movement keys. Typing something will start the
search and update the list (vim like interactive search). Only single selection
is supported. See [Key Bindings](#keyBindings) for more.

Software requirement:

This python script requires urwid version 1.1.1 (one of the python curses
library). Download urwid from http://excess.org/urwid and untar it and then
update the PYTHONPATH. This script also requires python argparse module.
Ubuntu has package called python-urwid but that is old and PSS does not support
it.

<a id="keyBindings"><a>Key Bindings:
```
Select and Quit:
mouse      : selects an item (no quitting)
enter      : write selection to given file and quit
esc        : quit only (no selection writing)
ctrl-x     : same as esc, but seems to a little faster on the terminal

Movements:
up         : Move up
down       : Move down
ctrl-p     : same as Up
ctrl-n     : same as Down

Search:
Everthing else. Just type and search.
```
Usage:
````
usage: pss.py [-h] -f FILE -l [line [line ...]]

Interactive search and selection of ASCII lines using python

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File to write the user selection.
  -l [line [line ...]], --lines [line [line ...]]
                        Lines to be displayed interactively to the user
```
Examples:

Simple Usage:

This command will open full screen Curses-based terminal session. And then
depending on the user selection, the user selection will be written to the file
specified in -f argument of the command.

pss.py -f ~/.result -l line1 line2 line3

Advanced Usage:

pss.py is useful when you create wrappers over it. I was using it to
interactively select my clearcase views using the myviews function given below
in my .bashrc

```bash
function myviews()
{
    resultFile=~/.selectedview
    # clear any previous selection.
    cat /dev/null > $resultFile
    allViews=$(cleartool lsview -short | grep $LOGNAME)
    # pss.py shall be in your $PATH
    pss.py -f $resultFile -l $allViews
    # if file has some contents
    if [[ -s $resultFile ]]; then
        cleartool setview $(cat $resultFile)
    fi
}
```
Also look at the examples dir to see the advanced usage.
