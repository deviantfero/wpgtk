from ..data import keywords
from ..data import files
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

        self.selected_file = ""
        wallpaper_list = Gtk.ListStore(str)
        for elem in list(files.get_file_list()):
            wallpaper_list.append([elem])

        self.liststore = Gtk.ListStore(str, str)
        self.reload_keyword_list()

        self.wallpaper_combo = Gtk.ComboBox.new_with_model(wallpaper_list)
        self.renderer_text = Gtk.CellRendererText()
        self.wallpaper_combo.pack_start(self.renderer_text, True)
        self.wallpaper_combo.add_attribute(self.renderer_text, "text", 0)
        self.wallpaper_combo.set_entry_text_column(0)
        self.wallpaper_combo.connect("changed", self.on_wallpaper_change)

        self.status_lbl = Gtk.Label('')
        self.keyword_tree = Gtk.TreeView(model=self.liststore)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(400)
        scroll.add(self.keyword_tree)

        self.attach(self.wallpaper_combo, 0, 0, 2, 1)
        self.attach(self.add_button, 0, 1, 1, 1)
        self.attach(self.delete_button, 1, 1, 1, 1)
        self.attach(scroll, 0, 2, 2, 1)
        self.attach(self.status_lbl, 0, 3, 2, 1)

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

    def remove_keyword(self, widget):
        self.status_lbl.set_text('')
        (m, pathlist) = self.keyword_tree.get_selection().get_selected_rows()

        for path in pathlist:
            tree_iter = m.get_iter(path)
            value = m.get_value(tree_iter, 0)
            keywords.remove_pair(self.selected_file, value)
            self.reload_keyword_list()

    def text_edited(self, widget, path, text, col):
        self.status_lbl.set_text('')
        if(col == 0):
            try:
                keywords.update_key(
                    self.selected_file,
                    self.liststore[path][col],
                    text
                )
            except Exception as e:
                self.status_lbl.set_text(str(e))
        else:
            try:
                keywords.update_value(
                    self.selected_file,
                    self.liststore[path][0],
                    text
                )
            except Exception as e:
                self.status_lbl.set_text(str(e))
        self.reload_keyword_list()

    def reload_keyword_list(self):
        self.liststore.clear()
        parser = keywords.get_keywords_parser(self.selected_file)
        for k, v in parser['keywords'].items():
            self.liststore.append([k, v])

    def on_wallpaper_change(self, widget):
        x = widget.get_active()

        current_walls = files.get_file_list()
        self.selected_file = current_walls[x]
        self.reload_keyword_list()

    def append_new_keyword(self, widget):
        self.status_lbl.set_text('')
        keywords.create_pair(
            self.selected_file,
            'keyword' + str(len(self.liststore)),
            'value'
        )
        self.reload_keyword_list()
