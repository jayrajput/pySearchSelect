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
logging.basicConfig(filename='/tmp/pysearchselect.log', filemode='w', level=logging.DEBUG)
#logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

def isQuickSelect(input):
    logging.debug("Inside function isQuickSelect, Input (%s)", input)
    # input len is 2 when user presses up arrow at the first element in
    # the list.
    if (len(input) == 1):
        logging.debug("Inside function isQuickSelect, ord(Input) (%s)", ord(input))
        if ord(input) in range(ord('0'), ord('9') + 1):
            return True
        elif ord(input) in range(ord('a'), ord('z') + 1):
            return True
    return False

def quickSelect2Int(input):
    logging.debug("Inside function quickSelect2Int, Input (%s)", input)
    if input.isdigit():
        return ord(input) - ord('0')
    elif input.isalpha():
        return ord(input) - ord('a') + 10

def int2QuickSelect(index):
    if index in range(0, 10):
        return str(index);
    elif index in range(10, 36):
        return chr(index + ord('a') - 10)
    else:
        # return space so that the digits are aligned.
        return " "

class ItemWidget (urwid.WidgetWrap):
    def __init__ (self, index, description):
        # store the content which can be extracted.
        self.content = '%s' % (description[0:])
        self.__super.__init__(
            urwid.Columns([
                urwid.AttrWrap(
                    urwid.Text(int2QuickSelect(index) + " " + description), 
                    'body', 
                    'focus'
                ),
            ])
        )
    #  to make a list, it have to be selectable, otherwise when you scroll, it
    #  will behave like a web browser, it will scroll the screen as soon as
    #  you press the down key, instead to go through every item of the screen before.
    def selectable (self):
        return True
    def keypress(self, size, key):
        return key

class CustomEdit(urwid.Edit):
    __metaclass__ = urwid.signals.MetaSignals
    signals = ['done']

    def keypress(self, size, key):
        logging.debug("Inside function keypress," + 
           "size (%s), key(%s)", size, key
        )
        urwid.Edit.keypress(self, size, key)
        urwid.emit_signal(self, 'done', self.get_edit_text())

class MyApp(object):
    def __init__(self, data):
        palette = [
            ('body'  , 'yellow' , 'black'       ) ,
            ('focus' , 'black'  , 'light green' ) ,
            ('head'  , 'yellow' , 'black'       ) ,
        ]
        self.insertMode = False
        self.file   = data["file"]
        self.items  = data["lines"]
        self.head   = CustomEdit('[Cmd]')
        header      = urwid.AttrMap(self.head, 'head')
        self.walker = urwid.SimpleListWalker([
                # python list comprehension. See
                # http://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
                ItemWidget(index, item) for (index, item) in enumerate(data["lines"])
            ]
        )
        self.listbox = urwid.ListBox(self.walker)
        self.view = urwid.Frame(
            urwid.AttrWrap(
                self.listbox,
                'body'
            ),
            header=None,
            footer=header,
            focus_part='body'
        )

        loop = urwid.MainLoop(
            self.view,
            palette,
            unhandled_input=self.keystroke
        )
        urwid.connect_signal(self.head, 'change', self.edit_change)
        urwid.connect_signal(self.head, 'done', self.edit_done)
        loop.run()

    def keystroke (self, input):
        logging.debug("Inside function keystroke, Input (%s)", input)
        # the is does not work here, so end up using in
        if input in ('ctrl n', 'ctrl N'):
            try:
                (junk, focus) = self.walker.get_focus()
                self.walker.set_focus(self.walker.next_position(focus))
            except (IndexError):
                pass
        elif input in ('ctrl p', 'ctrl P'):
            try:
                (junk, focus) = self.walker.get_focus()
                self.walker.set_focus(self.walker.prev_position(focus))
            except (IndexError):
                pass
        elif input is 'esc':
            raise urwid.ExitMainLoop()
        elif input is 'enter':
            fh = open(self.file, "w")
            fh.write(self.listbox.get_focus()[0].content)
            fh.close()
            raise urwid.ExitMainLoop()
        elif input in ('/', 'tab'):
            self.insertMode = not self.insertMode
            if self.insertMode:
                self.head.set_caption('[Ins]')
            else:
                self.head.set_caption('[Cmd]')
        elif self.insertMode:
                if not isinstance(input, tuple):
                    self.head.keypress((20,), input)
        elif isQuickSelect(input):
            self.walker.set_focus(quickSelect2Int(input))


    def edit_change(self, input, content):
        # strip any asterisk before adding ours.
        content = "*" + content.strip("*") + "*"
        # list comprehension again.
        # See http://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
        visibleItems = [
            item
            for item in self.items
            if fnmatch.fnmatch(item, content)
        ]
        self.walker[:] = [
            ItemWidget(index, item)
            for (index, item) in enumerate(visibleItems)
        ]

    def edit_done(self, content):
        self.view.set_focus('body')

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
    args = parser.parse_args()
    MyApp({
        "file" : args.file,
        "lines" : args.inLines
    })

