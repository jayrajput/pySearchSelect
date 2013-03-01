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


def isQuickSelect(input):
    return input.isalnum()

def quickSelect2Int(input):
    if input.isdigit():
        return ord(input) - 48
    elif input.isalpha():
        # ord('a') = 97 
        return ord(input) - 87

def int2QuickSelect(index):
    if index in range(0, 10):
        return str(index);
    elif index in range(10, 36):
        # chr(97) = 'a'
        return chr(index + 87)
    else:
        return ""

class ItemWidget (urwid.WidgetWrap):
    def __init__ (self, index, description):
        self.index = index
        self.content = '%s' % (description[0:])
        self.item = [
            (
                'fixed', 
                4, 
                urwid.Padding(
                    urwid.AttrWrap(
                        urwid.Text('%s' % int2QuickSelect(index)), 
                        'body', 
                        'focus'
                    ), 
                    left=1
                )
            ),
            urwid.AttrWrap(
                urwid.Text('%s' % description), 
                'body', 
                'focus'
            ),
        ]
        w = urwid.Columns(self.item)
        self.__super.__init__(w)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key

class CustomEdit(urwid.Edit):
    __metaclass__ = urwid.signals.MetaSignals
    signals = ['done']

    def keypress(self, size, key):
        if key in ('enter','tab', 'down', 'up', 'ctrl n'):
            urwid.emit_signal(self, 'done', self.get_edit_text())
            return
        elif key == 'esc':
            urwid.emit_signal(self, 'done', None)
            return
        urwid.Edit.keypress(self, size, key)

class MyApp(object):
    def __init__(self, data):
        palette = [
            ('body'  , 'yellow' , 'black'       ) ,
            ('focus' , 'black'  , 'light green' ) ,
            ('head'  , 'yellow' , 'black'       ) ,
        ]
        self.file   = data["file"]
        self.items  = data["lines"]
        self.head   = CustomEdit('/')
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
            header=header,
            footer=None,
            focus_part='header'
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
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif input is 'enter':
            fh = open(self.file, "w")
            fh.write(self.listbox.get_focus()[0].content)
            fh.close()
            raise urwid.ExitMainLoop()
        elif input in ('/', 'tab'):
            self.view.set_focus('header')
        elif isQuickSelect(input):
            self.walker.set_focus(quickSelect2Int(input))
        elif input is "ctrl n":
            self.walker.set_focus(self.walker.next_position()+ 1)



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

