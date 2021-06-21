from ..data import keywords
from ..data import files
from ..data.config import KEYWORD_DIR
from gi import require_version
from gi.repository import Gtk
require_version("Gtk", "3.0")

PAD = 10

class KeywordGrid(Gtk.Grid):
    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.parent = parent

        self.set_border_width(PAD)
        self.set_column_homogeneous(1)
        self.set_row_spacing(PAD)
        self.set_column_spacing(PAD)

        self.delete_button = Gtk.Button('Remove')
        self.delete_button.connect('clicked', self.remove_keyword)

        self.add_button = Gtk.Button('Add')
        self.add_button.connect('clicked', self.append_new_keyword)

        self.reset_button = Gtk.Button('Reset')
        # self.reset_button.connect('clicked', self.reset_keyword_file)

        self.create_button = Gtk.Button('Create')
        self.create_button.connect('clicked', self.on_create_click)

        self.selected_file = None
        self.keyword_file_combo = Gtk.ComboBoxText()
        self.keyword_file_combo.set_entry_text_column(0)
        self.keyword_file_combo.append_text('Default')
        for elem in list(files.get_file_list(KEYWORD_DIR, False)):
            self.keyword_file_combo.append_text(elem)

        self.keyword_file_combo.set_active(0)

        self.liststore = Gtk.ListStore(str, str)
        self.reload_keyword_list()

        self.keyword_file_combo.set_entry_text_column(0)
        self.keyword_file_combo.connect("changed", self.on_keyword_file_change)

        self.status_lbl = Gtk.Label('')
        self.keyword_tree = Gtk.TreeView(model=self.liststore)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(400)
        scroll.add(self.keyword_tree)

        self.attach(self.keyword_file_combo, 0, 0, 2, 1)
        self.attach(self.create_button, 2, 0, 1, 1)
        self.attach(self.add_button, 0, 1, 1, 1)
        self.attach(self.delete_button, 1, 1, 1, 1)
        self.attach(self.reset_button, 2, 1, 1, 1)
        self.attach(scroll, 0, 2, 3, 1)
        self.attach(self.status_lbl, 0, 3, 3, 1)

        key_renderer = Gtk.CellRendererText()
        key_renderer.set_property('editable', True)
        key_renderer.connect('edited', self.text_edited, 0)

        value_renderer = Gtk.CellRendererText()
        value_renderer.set_property('editable', True)
        value_renderer.connect('edited', self.text_edited, 1)

        keyword_text = Gtk.TreeViewColumn("Keyword", key_renderer, text=0)
        self.keyword_tree.append_column(keyword_text)

        value_text = Gtk.TreeViewColumn("Value", value_renderer, text=1)
        self.keyword_tree.append_column(value_text)

    def on_create_click(self, widget):
        filechooser = Gtk.FileChooserDialog(
                      'Create Config File', self.parent,
                      Gtk.FileChooserAction.SAVE,
                      (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                       Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        file_filter = Gtk.FileFilter()
        file_filter.set_name("Conf")
        file_filter.add_mime_type("text/plain")
        file_filter.add_pattern("*.conf")
        filechooser.add_filter(file_filter)
        filechooser.set_current_folder(KEYWORD_DIR)
        response = filechooser.run()
        print(filechooser.get_filename())
        print(response)
        filechooser.destroy()

    def remove_keyword(self, widget):
        self.status_lbl.set_text('')
        (m, pathlist) = self.keyword_tree.get_selection().get_selected_rows()

        for path in pathlist:
            tree_iter = m.get_iter(path)
            value = m.get_value(tree_iter, 0)
            keywords.remove_pair(value, self.selected_file)
            self.reload_keyword_list()

    def text_edited(self, widget, path, text, col):
        self.status_lbl.set_text('')
        if (col == 0):
            try:
                keywords.update_key(self.liststore[path][col], text,
                                    self.selected_file)
            except Exception as e:
                self.status_lbl.set_text(str(e))
        else:
            try:
                keywords.update_value(self.liststore[path][0], text,
                                      self.selected_file)
            except Exception as e:
                self.status_lbl.set_text(str(e))
        self.reload_keyword_list()

    def reload_keyword_list(self):
        keyword_section = keywords.get_keywords_section(self.selected_file)

        self.liststore.clear()
        for k, v in keyword_section.items():
            self.liststore.append([k, v])

    def on_keyword_file_change(self, widget):
        selected_entry = widget.get_active_text()
        self.selected_file = None if selected_entry == 'Default' else selected_entry
        self.reload_keyword_list()

    def append_new_keyword(self, widget):
        self.status_lbl.set_text('')
        keywords.create_pair(
            'keyword' + str(len(self.liststore)),
            'value',
            self.selected_file,
        )
        self.reload_keyword_list()
