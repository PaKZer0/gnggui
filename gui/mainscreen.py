import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GnGGladeGui():
	def run(self):
		builder = Gtk.Builder()
		builder.add_from_file("gui/gngui.glade")
		builder.connect_signals(Handler())

		window = builder.get_object("window1")
		window.show_all()
		window.connect("destroy", Gtk.main_quit)

		Gtk.main()


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

if __name__ == '__main__':
    GnGGladeGui().run()
