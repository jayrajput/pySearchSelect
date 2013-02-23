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

class ItemWidget (urwid.WidgetWrap):
    def __init__ (self, description):
        self.description = urwid.Text(description)
        self.item = [
            urwid.AttrWrap(self.description, 'body', 'focus'),
        ]
        self.content = '%s' % (description[:45])
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
        if key in ('enter','tab', 'down', 'up'):
            urwid.emit_signal(self, 'done', self.get_edit_text())
            return
        elif key == 'esc':
            urwid.emit_signal(self, 'done', None)
            return
        urwid.Edit.keypress(self, size, key)

class MyApp(object):
    def __init__(self):
        palette = [
            ('body'  , 'yellow' , 'black'       ) ,
            ('focus' , 'black'  , 'light green' ) ,
            ('head'  , 'yellow' , 'black'       ) ,
        ]
        self.items  = args.inLines
        self.head   = CustomEdit('/')
        header      = urwid.AttrMap(self.head, 'head')
        self.walker = urwid.SimpleListWalker(
            # python list comprehension. See
            # http://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
            [ItemWidget(str(line)) for line in args.inLines]
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
            fh = open(args.file, "w")
            fh.write(self.listbox.get_focus()[0].content)
            fh.close()
            raise urwid.ExitMainLoop()
        elif input in ('/', 'tab'):
            self.view.set_focus('header')

    def edit_change(self, input, content):
        # strip any asterisk before adding ours.
        content = "*" + content.strip("*") + "*"
        # list comprehension again.
        # See http://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
        self.walker[:] = [ItemWidget(item) for item in self.items if fnmatch.fnmatch(item, content)]

    def edit_done(self, content):
        self.view.set_focus('body')

if __name__ == '__main__':
    def parseCmdLineArgs():
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
        return parser.parse_args()

    args = parseCmdLineArgs()
    MyApp()
