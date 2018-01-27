from gi import require_version
from . import color_grid, template_grid
from . import option_grid, keyword_grid
from wpgtk.data import files, themer, config
from gi.repository import Gtk, GdkPixbuf
import os
require_version('Gtk', '3.0')

PAD = 10


class mainWindow(Gtk.Window):

    def __init__(self, args):
        Gtk.Window.__init__(self, title='wpgtk ' + config.__version__)

        image_name = os.path.join(config.WPG_DIR, '.current')
        image_name = os.path.realpath(image_name)
        self.set_default_size(200, 200)
        self.args = args

        # these variables are just to get the image
        # and preview of current wallpaper
        file_name = themer.get_current()
        print('INF::CURRENT WALL: ' + file_name)
        sample_name = os.path.join(config.SAMPLE_DIR,
                                   (file_name + '.sample.png'))

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.wpage = Gtk.Grid()
        self.wpage.set_border_width(PAD)
        self.wpage.set_column_homogeneous(1)
        self.wpage.set_row_spacing(PAD)
        self.wpage.set_column_spacing(PAD)

        self.cpage = color_grid.ColorGrid(self)
        self.fpage = template_grid.TemplateGrid(self)
        self.optpage = option_grid.OptionsGrid(self)
        self.keypage = keyword_grid.KeywordGrid(self)

        self.notebook.append_page(self.wpage, Gtk.Label('Wallpapers'))
        self.notebook.append_page(self.cpage, Gtk.Label('Colors'))
        self.notebook.append_page(self.fpage, Gtk.Label('Templates'))
        self.notebook.append_page(self.keypage, Gtk.Label('Keywords'))
        self.notebook.append_page(self.optpage, Gtk.Label('Options'))

        option_list = Gtk.ListStore(str)
        for elem in list(files.get_file_list()):
            option_list.append([elem])
        self.option_combo = Gtk.ComboBox.new_with_model(option_list)
        self.renderer_text = Gtk.CellRendererText()
        self.option_combo.pack_start(self.renderer_text, True)
        self.option_combo.add_attribute(self.renderer_text, 'text', 0)
        self.option_combo.set_entry_text_column(0)

        self.textbox = Gtk.Label()
        self.textbox.set_text('Select colorscheme')
        self.colorscheme = Gtk.ComboBox.new_with_model(option_list)
        self.colorscheme.pack_start(self.renderer_text, True)
        self.colorscheme.add_attribute(self.renderer_text, 'text', 0)
        self.colorscheme.set_entry_text_column(0)

        self.set_border_width(10)
        # another container will be added so this will probably change
        # self.add(self.wpage)
        self.preview = Gtk.Image()
        self.sample = Gtk.Image()

        if(os.path.isfile(image_name) and os.path.isfile(sample_name)):
            self.pixbuf_preview = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                                  image_name,
                                  width=500,
                                  height=333, preserve_aspect_ratio=False)
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size(
                                 sample_name,
                                 width=500, height=500)
            self.preview.set_from_pixbuf(self.pixbuf_preview)
            self.sample.set_from_pixbuf(self.pixbuf_sample)

        self.add_button = Gtk.Button(label='Add')
        self.set_button = Gtk.Button(label='Set')
        self.set_button.set_sensitive(False)
        self.rm_button = Gtk.Button(label='Remove')
        # adds to first cell in wpage
        self.wpage.attach(self.option_combo, 1, 1, 2, 1)
        self.wpage.attach(self.colorscheme, 1, 2, 2, 1)
        self.wpage.attach(self.set_button, 3, 1, 1, 1)
        self.wpage.attach(self.add_button, 3, 2, 2, 1)
        self.wpage.attach(self.rm_button, 4, 1, 1, 1)
        self.wpage.attach(self.preview, 1, 3, 4, 1)
        self.wpage.attach(self.sample, 1, 4, 4, 1)
        self.add_button.connect('clicked', self.on_add_clicked)
        self.set_button.connect('clicked', self.on_set_clicked)
        self.rm_button.connect('clicked', self.on_rm_clicked)
        self.option_combo.connect('changed', self.combo_box_change)
        self.colorscheme.connect('changed', self.colorscheme_box_change)
        self.entry = Gtk.Entry()
        self.current_walls = Gtk.ComboBox()

    def on_add_clicked(self, widget):
        filepath = ""
        filechooser = Gtk.FileChooserDialog(
                      'Select an Image', self,
                      Gtk.FileChooserAction.OPEN,
                      (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                       Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filefilter = Gtk.FileFilter()
        filefilter.set_name("Images")
        filefilter.add_mime_type("image/png")
        filefilter.add_mime_type("image/jpg")
        filefilter.add_mime_type("image/jpeg")
        filechooser.add_filter(filefilter)
        response = filechooser.run()

        if response == Gtk.ResponseType.OK:
            filepath = filechooser.get_filename()
        filechooser.destroy()

        themer.create_theme(filepath)
        option_list = Gtk.ListStore(str)

        for elem in list(files.get_file_list()):
            option_list.append([elem])
        self.option_combo.set_model(option_list)
        self.option_combo.set_entry_text_column(0)
        self.colorscheme.set_model(option_list)
        self.colorscheme.set_entry_text_column(0)
        self.cpage.update_combo(option_list)

    def on_set_clicked(self, widget):
        x = self.option_combo.get_active()
        y = self.colorscheme.get_active()
        current_walls = files.get_file_list()
        if current_walls:
            filename = current_walls[x]
            colorscheme_file = current_walls[y]
            themer.set_theme(filename, colorscheme_file)

    def on_rm_clicked(self, widget):
        x = self.option_combo.get_active()
        current_walls = files.get_file_list()
        if current_walls:
            filename = current_walls[x]
            themer.delete_theme(filename)
            option_list = Gtk.ListStore(str)
            for elem in list(files.get_file_list()):
                option_list.append([elem])
            self.option_combo.set_model(option_list)
            self.option_combo.set_entry_text_column(0)
            self.colorscheme.set_model(option_list)
            self.colorscheme.set_entry_text_column(0)
            self.cpage.update_combo(option_list)

    def combo_box_change(self, widget):
        self.set_button.set_sensitive(True)
        x = self.option_combo.get_active()
        self.colorscheme.set_active(x)
        selected_file = files.get_file_list()[x]
        filepath = os.path.join(config.WALL_DIR, selected_file)

        self.pixbuf_preview = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            str(filepath),
            width=500,
            height=333,
            preserve_aspect_ratio=False)
        self.preview.set_from_pixbuf(self.pixbuf_preview)

    def colorscheme_box_change(self, widget):
        x = self.colorscheme.get_active()
        selected_file = files.get_file_list()[x]
        samplepath = os.path.join(config.SAMPLE_DIR,
                                  (selected_file + '.sample.png'))
        if(os.path.isfile(samplepath)):
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size(
                                 samplepath, width=500, height=500)
        self.sample.set_from_pixbuf(self.pixbuf_sample)
        self.cpage.set_edit_combo(x)


def run(args):
    win = mainWindow(args)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    run()
