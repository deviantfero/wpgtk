import logging
from ..data import keywords
from ..data.config import user_keywords, settings, write_conf
from gi import require_version
require_version("Gtk", "3.0")
from .keyword_dialog import KeywordDialog  # noqa: E402
from gi.repository import Gtk  # noqa: E402

PAD = 10

# TODO: if create section, select the new valid section


class KeywordGrid(Gtk.Grid):
    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.parent = parent

        self.set_border_width(PAD)
        self.set_column_homogeneous(1)
        self.set_row_spacing(PAD)
        self.set_column_spacing(PAD)

        self.liststore = Gtk.ListStore(str, str)

        self.remove_button = Gtk.Button('Remove Keyword')
        self.remove_button.connect('clicked', self.remove_keyword)

        self.add_button = Gtk.Button('Add Keyword')
        self.add_button.connect('clicked', self.append_new_keyword)

        self.choose_button = Gtk.Button('Choose Set')
        self.choose_button.connect('clicked', self.choose_keywords_section)

        self.create_button = Gtk.Button('Create Set')
        self.create_button.connect('clicked', self.create_keywords_section)

        self.delete_button = Gtk.Button('Delete Set')
        self.delete_button.connect('clicked', self.delete_keywords_section)

        self.sections_combo = Gtk.ComboBoxText()
        self.sections_combo.connect("changed", self.on_section_change)
        self.reload_section_list()

        self.selected_file = settings.get("keywords", "default")
        idx = list(user_keywords.sections()).index(self.selected_file)
        self.sections_combo.set_active(idx)
        self.delete_button.set_sensitive(self.selected_file != 'default')
        self.choose_button.set_sensitive(False)

        self.reload_keyword_list()

        self.status_lbl = Gtk.Label('')
        self.keyword_tree = Gtk.TreeView(model=self.liststore)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(320)
        scroll.set_propagate_natural_height(True)
        scroll.add(self.keyword_tree)

        self.attach(self.sections_combo, 0, 0, 2, 1)
        self.attach(self.choose_button, 2, 0, 1, 1)
        self.attach(self.delete_button, 3, 0, 1, 1)
        self.attach(self.create_button, 0, 1, 4, 1)
        self.attach(scroll, 0, 2, 4, 1)
        self.attach(self.add_button, 0, 3, 2, 1)
        self.attach(self.remove_button, 2, 3, 2, 1)
        self.attach(self.status_lbl, 0, 4, 4, 1)

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

    def reload_section_list(self, active='default'):
        sections = list(user_keywords.sections())
        self.sections_combo.remove_all()

        for item in sections:
            self.sections_combo.append_text(item)

        self.sections_combo.set_active(sections.index(active))

    def reload_keyword_list(self):
        keyword_section = keywords.get_keywords_section(self.selected_file)

        self.liststore.clear()
        for k, v in keyword_section.items():
            self.liststore.append([k, v])

    def on_section_change(self, widget):
        self.selected_file = widget.get_active_text()

        if self.selected_file is not None:
            self.reload_keyword_list()
            self.choose_button.set_sensitive(
                settings.get('keywords', 'default') != self.selected_file
            )
            settings['keywords'] = self.selected_file
            self.delete_button.set_sensitive(self.selected_file != 'default')

    def append_new_keyword(self, widget):
        self.status_lbl.set_text('')
        keywords.create_pair(
            'keyword' + str(len(self.liststore)),
            'value',
            self.selected_file,
        )
        self.reload_keyword_list()

    def delete_keywords_section(self, widget):
        if self.selected_file:
            keywords.delete_keywords_section(self.selected_file)
            self.reload_section_list()

    def choose_keywords_section(self, widget):
        write_conf()
        self.choose_button.set_sensitive(False)

    def create_keywords_section(self, widget):
        dialog = KeywordDialog(self.parent)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            try:
                section = dialog.get_section_name()
                keywords.create_keywords_section(section)
                self.reload_section_list(section)
            except Exception as e:
                logging.error(str(e))
            dialog.destroy()
        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
