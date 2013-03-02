#!/usr/bin/python

# @author Jay Rajput.
# @email  jayrajput@gmail.com
# @See    http://www.nicosphere.net/selectable-list-with-urwid-for-python-2542/

# python curses library. @See http://excess.org/urwid/
import urwid
# Needed for command line parsing.
import argparse
# use unix like file name matching.
import fnmatch 
# python logging
import logging

# http://docs.python.org/2/howto/logging.html#logging-basic-tutorial
# redirect logging to a /tmp file
# Uncomment to see the keystroke logged
# logging.basicConfig(filename='/tmp/pysearchselect.log', filemode='w', level=logging.DEBUG)
# logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

class ItemWidget (urwid.WidgetWrap):
    def __init__ (self, content):
        # store the content which can be extracted later when this widget is
        # selected.
        self.content = content
        self.__super.__init__(
            urwid.AttrWrap(
                urwid.Text(content), 
                # palette is defined in MyApp::init
                'body', 
                'focus'
            )
        )
    # allow mouse selection.
    def selectable(focus):
        return True
    # keypress flow from inner objects to outer objects.
    # keypress is handled in outer object
    def keypress(self, size, key):
        return key

class MyApp(object):
    def __init__(self, data):
        """ 
        create the urwid widgets and starts urwid main loop
        input argument is a dictionary
        {
            "file"  : "/tmp/1"
            "lines" : [
                "line 1",
                "line 2",
                "line 3"
            ],
            # optional search string.
            "search" : "2",
        }
        """
        # this is used to write the selection.
        self.file   = data.get("file")
        # used for performing search.
        self.items  = data.get("lines")

        if self.file is None or self.items is None:
            raise ValueError("Mandatory arguments (file and lines) missing.")

        # urwid specific widgets.
        # footer to erase and set value on search.
        self.foot   = urwid.Edit("/")
        # walker to add /remove content from the listbox.
        self.walker = urwid.SimpleListWalker([
            # python list comprehension. See
            # http://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
            ItemWidget(item) for item in data["lines"]
        ])


        loop = urwid.MainLoop(
            # urwid.Frame is a box widget containing header, body and
            # footer. We are not using header.
            urwid.Frame(
                # List Box is again a box widget which can contain list of flow
                # widgets (our ItemWidget in this case).
                urwid.ListBox(self.walker),
                header=None,
                footer=self.foot,
                focus_part='body'
            ),
            [
                # palette is similar to one used by dmenu.
                # use white on black when not in focus.
                ('body'  , 'white' , 'black'    ) ,
                # use white on dark cyan when in focus.
                ('focus' , 'white' , 'dark cyan') ,
            ],
            unhandled_input=self.keystroke
        )
        urwid.connect_signal(self.foot, 'change', self.editChange)

        # filter the list if requested by the user.
        search = data.get("search")
        if search is not None:
            self.foot.set_edit_text(search)
            self.foot.set_edit_pos(len(search))

        loop.run()

    def keystroke (self, input):
        """ handle keystroke for movement, quit, select, search """
        logging.debug("Inside function keystroke, Input (%s)", input)
        # Movement
        if input in ('ctrl n', 'ctrl N'):
            try:
                (junk, focus) = self.walker.get_focus()
                if focus is not None:
                    self.walker.set_focus(self.walker.next_position(focus))
            except (IndexError):
                # When at the end of the list.
                pass
        elif input in ('ctrl p', 'ctrl P'):
            try:
                (junk, focus) = self.walker.get_focus()
                if focus is not None:
                    self.walker.set_focus(self.walker.prev_position(focus))
            except (IndexError):
                # When at the top of the list.
                pass
        # Quit
        elif input in ('esc', 'ctrl x'):
            raise urwid.ExitMainLoop()
        # Select
        elif input is 'enter':
            focus=self.walker.get_focus()
            if focus[0] is not None:
                fh = open(self.file, "w")
                fh.write(focus[0].content)
                fh.close()
                raise urwid.ExitMainLoop()
        # Search
        elif not isinstance(input, tuple):
            # if input is something other than the mouse.
            # mouse inputs are tuples e.g
            # Input (('mouse press', 1, 3, 15))
            # Input (('mouse release', 0, 3, 15))
            # pass on the keyboard characters to the edit box.
            # size 20 is choosen for large keys like backspace??
            self.foot.keypress((20,), input)
        # Anything else
        else:
            pass

    def editChange(self, input, content):
        """ update the widgets in the body depending on search string."""
        # list comprehension again.
        # See http://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
        self.walker[:] = [
            ItemWidget(item) for item in self.items
            if fnmatch.fnmatch(
                item, 
                # strip any asterisk before adding ours.
                "*" + content.strip("*") + "*"
            )
        ]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Interactive search and selection of ASCII lines using python'
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help='File to write the user selection.',
        dest='file'
    )
    parser.add_argument(
        "-l", "--lines",
        required=True,
        nargs='*',
        help='Lines to be displayed interactively to the user',
        dest='inLines',
        metavar='line'
    )
    # if a value is not provided, argparse set the default of searchStr to
    # None.
    parser.add_argument(
        "-s", "--search",
        required=False,
        help='Intial search string to filter the list',
        dest='search'
    )
    args = parser.parse_args()
    MyApp({
        "file"   : args.file,
        "lines"  : args.inLines,
        "search" : args.search
    })
