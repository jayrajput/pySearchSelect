viewSearchSelect
================

bash script to interactively search and select cleartool views. I have written this 
script to interactively select my clearcase views.  This
script passes a list of views to the pySearchSelect command to show a full
screen curses based menu to the user to search and select a view. The list
contains the most recently used views followed by others. This script keep track
of the most recently views.

Responsibility of this script:
- Manage the list of all views in allView file.
- Manage the list of MRU views in mruView file.
- Periodically update the above two list.

This script will create allView and mruView needed by this script under
~/.viewSearchSelect.

Responsibility of pySearchSelect is to provide a GUI for search and selection
of views.

Cleartool terminology/commands:
- cleartool setview <view> : Set the given view.
- cleartool lsview -short  : Show the short name for all the views on the system.



