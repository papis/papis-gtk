import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk


import re
import papis.utils
import papis.config
import papis.database
import papis.commands.open


class ListElement(Gtk.Label):

    def __init__(self, document):
        Gtk.Label.__init__(self)
        self.document = document
        self.match_format = papis.utils.format_doc(
            papis.config.get('match-format'), document
        )
        self.set_markup(
            papis.utils.format_doc(
                papis.config.get('header-format', section='rofi-gui'),
                self.document
            )
        )
        self.set_yalign(0.0)
        self.set_xalign(0.0)
        self.set_line_wrap(10.0)
        self.set_properties('can-focus', True)
        self.set_properties('has-focus', True)
        self.set_properties('has-tooltip', True)
        self.set_properties('tooltip-text', 'asf')
        self.set_properties('focus-padding', 20)

    def get_document(self):
        return self.document

    def get_match_format(self):
        return self.match_format

class ElementList(Gtk.ListBox):

    def __init__(self, search_widget):
        Gtk.ListBox.__init__(self)

        self.search_widget = search_widget

        def filtering(el):
            m = el.get_children()[0].get_match_format()
            return re.match(
                '.*'+re.sub('  *', '\s*', self.search_widget.get_text()),
                m,
                re.I
            )

        self.set_filter_func(filtering)

        self.connect("key-press-event", self.handle_key)

    def handle_key(self, w, event):
        if key_pressed_is(event, 'o'):
            doc = self.get_selected_document()
            papis.commands.open.run(doc)

    def get_selected_index(self):
        return self.get_selected_row().get_index()

    def get_selected_document(self):
        return self.get_selected_row().get_children()[0].get_document()

    def clear(self):
        print('clearing')
        for el in self.get_children():
            self.remove(el)

    def update(self, documents):
        print('updating')
        for doc in documents:
            el = ListElement(doc)
            self.add(el)
            el.show()


def key_pressed_is(event, key_string):
    """Vim like binding language
    """
    import re
    ctrl = re.match(r'^<Ctrl-(.)>$', key_string, re.I)
    ctrl_shift = re.match(r'^<Ctrl-S-(.)>$', key_string, re.I)
    alt = re.match(r'^<Alt-(.)>$', key_string, re.I)
    lower_key = re.match(r'^(.)$', key_string, re.I)
    upper_key = re.match(r'^<S-(.)>$', key_string, re.I)
    if ctrl:
        return (
            Gdk.ModifierType.CONTROL_MASK & event.state and
            not Gdk.ModifierType.SHIFT_MASK & event.state and
            event.keyval == Gdk.keyval_from_name(ctrl.group(1).lower())
        )
    if ctrl_shift:
        return (
            Gdk.ModifierType.CONTROL_MASK & event.state and
            Gdk.ModifierType.SHIFT_MASK & event.state and
            event.keyval == Gdk.keyval_from_name(ctrl_shift.group(1).upper())
        )
    elif lower_key:
        return (
            not Gdk.ModifierType.CONTROL_MASK & event.state and
            not Gdk.ModifierType.SHIFT_MASK & event.state and
            event.keyval == Gdk.keyval_from_name(lower_key.group(1).lower())
        )
    elif upper_key:
        return (
            not Gdk.ModifierType.CONTROL_MASK & event.state and
            Gdk.ModifierType.SHIFT_MASK & event.state and
            event.keyval == Gdk.keyval_from_name(upper_key.group(1).upper())
        )
    else:
        return False


class Gui(Gtk.Window):
    def __init__(self, documents=[], header_filter=None):

        Gtk.Window.__init__(self)
        self.lines = 50

        self.db = papis.database.get()

        self.set_decorated(False)
        self.set_title('Papis gtk picker')

        self.connect("key-press-event", self.handle_key)

        self.entry = Gtk.Entry()
        self.connect("key-release-event", self.handle_entry_key)
        self.entry.set_icon_from_icon_name(
            Gtk.EntryIconPosition(0),
            'search'
        )
        self.entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition(0),
            'Query input'
        )

        self.listbox = ElementList(self.entry)

        print('Vbox added')
        vbox = Gtk.VBox()
        vbox.add(self.entry)
        s = Gtk.ScrolledWindow()
        s.set_min_content_height(
            self.get_screen().get_height() * self.lines / 100
        )
        # s.set_max_content_height(
            # self.get_screen().get_height() * self.lines / 100
        # )
        s.add(self.listbox)

        vbox.add(s)


        self.add(vbox)
        self.show_all()
        self.move(0,0)
        self.resize(
            self.get_screen().get_width(),
            2
        )

        self.documents = documents
        if documents:
            self.listbox.update(documents)

        Gtk.main()

    def get(self):
        return self.listbox.get_selected_document()

    def get_selected_document(self):
        return self.listbox.get_selected_document()

    def focus_filter_prompt(self):
        self.entry.set_icon_from_icon_name(
            Gtk.EntryIconPosition(0),
            'search'
        )
        self.entry.grab_focus()

    def focus_query_prompt(self):
        a = Gtk.Window()
        entry = Gtk.Entry()
        entry.set_icon_from_icon_name(
            Gtk.EntryIconPosition(0),
            'server'
        )
        a.add(entry)
        a.show_all()
        entry.grab_focus()
        entry.get_text()

    def handle_entry_key(self, w, el):
        self.listbox.invalidate_filter()

    def handle_key(self, w, event):
        # print(event.get_keycode())
        # print(event.get_keyval())
        # print(event.string)
        # print(event.state)
        #enter
        if key_pressed_is(event, '<ctrl-s>'):
            self.focus_query_prompt()
        elif key_pressed_is(event, '<ctrl-f>'):
            print('\tfocusing')
            self.focus_filter_prompt()
        elif key_pressed_is(event, '<ctrl-c>'):
            self.listbox.clear()
        elif key_pressed_is(event, '<ctrl-u>'):
            self.listbox.update(self.documents)
        elif key_pressed_is(event, '<ctrl-q>'):
            Gtk.main_quit()


def pick(options, header_filter=None, body_filter=None, match_filter=None):
    return Gui(options, header_filter).get()
