from ..data.config import user_keywords, write_conf
from ..data import keywords
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

        self.liststore = Gtk.ListStore(str, str)
        self.reload_keyword_list()

        self.save_btn = Gtk.Button('Save')
        self.save_btn.connect('clicked', self.save_keywords)

        self.del_btn = Gtk.Button('Remove')
        self.del_btn.connect('clicked', self.remove_keyword)

        self.add_btn = Gtk.Button('Add')
        self.add_btn.connect('clicked', self.append_new_keyword)

        self.status_lbl = Gtk.Label('')

        self.keyword_tree = Gtk.TreeView(model=self.liststore)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(400)
        scroll.add(self.keyword_tree)

        self.attach(self.add_btn, 0, 0, 2, 1)
        self.attach(self.save_btn, 0, 1, 1, 1)
        self.attach(self.del_btn, 1, 1, 1, 1)
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
            user_keywords.pop(value, None)
            self.reload_keyword_list()

    def text_edited(self, widget, path, text, col):
        self.status_lbl.set_text('')
        if(col == 0):
            try:
                keywords.update_keyword(self.liststore[path][col], text)
            except Exception as e:
                self.status_lbl.set_text(str(e))
        else:
            try:
                keywords.update_value(self.liststore[path][0], text)
            except Exception as e:
                self.status_lbl.set_text(str(e))
        self.reload_keyword_list()

    def reload_keyword_list(self):
        self.liststore.clear()
        for k, v in user_keywords.items():
            self.liststore.append([k, v])

    def save_keywords(self, widget):
        write_conf()
        self.status_lbl.set_text('Saved')

    def append_new_keyword(self, widget):
        self.status_lbl.set_text('')
        keywords.create_pair('keyword' + str(len(self.liststore)), 'value')
        self.reload_keyword_list()
