import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from core.controller import Controller
from gui.abstractgui import AbstractGui

class GnGGladeGui(AbstractGui):
    def build(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui/gngui.glade")
    
    def bind_signals(self):
        ## window ##
        window = self.builder.get_object("window1")
        window.show_all()
        window.connect("destroy", Handler.onDestroy)
    
    def exit(self):
        super().exit()
        Gtk.main_quit()
    
    def get_partidas_options(self):
        partidas = self.con.get_partidas()
        ret = Gtk.ListStore(int, str)
        
        for partida in partidas:
            ret.append([partida.id, partida.nombre])
        
        return ret
    
    def load_partidas_combo(self):
        # cargar combo partida
        partidas_store = self.get_partidas_options()
        combo_partidas = self.builder.get_object("combo-partida")
        combo_partidas.set_model(partidas_store)
    
    def run(self):
        super().run()
        self.build()
        self.bind_signals()
        Gtk.main()
        
        # oscurecer otras pestañas
        tab1 = self.builder.get_object("tab-partida").set_sensitive(False)
        tab2 = self.builder.get_object("tab-equipo").set_sensitive(False) 
        tab3 = self.builder.get_object("tab-personaje").set_sensitive(False)
        tab4 = self.builder.get_object("tab-tiradas").set_sensitive(False)
        tab5 = self.builder.get_object("tab-combate").set_sensitive(False)
        

class Handler:
    def onDestroy(self, *args):
        gui = GnGGladeGui.get_instance()
        gui.exit()

def run_gui():
    gui = GnGGladeGui.get_instance()
    gui = gui.run()

if __name__ == '__main__':
    run_gui()
