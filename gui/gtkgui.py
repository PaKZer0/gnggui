import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import logging
from pprint import pprint

from core.controller import Controller
from gui.abstractgui import AbstractGui

logger = logging.getLogger(__name__)

class GnGGladeGui(AbstractGui):
    def build(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui/gngui.glade")

    def bind_signals(self):
        ## window ##
        window = self.builder.get_object("window1")
        window.connect("destroy", Handler.onDestroy)
        window.connect("show", Handler.onShowMain)
        window.show_all()

        ## tab seleccionar ##
        bnewpartida = self.builder.get_object("button-new-partida")
        bnewpartida.connect("clicked", Handler.onCrearPartida)

        bloadpartida = self.builder.get_object("button-load-partida")
        bloadpartida.connect("clicked", Handler.onSeleccionarPartida)

        brmpartida = self.builder.get_object("button-remove-partida")
        brmpartida.connect("clicked", Handler.onBorrarPartida)

        ## tab partida ##
        beditpartida = self.builder.get_object("button-edit-partida")
        beditpartida.connect("clicked", Handler.onEditPartida)

    def get_object(self, object_id):
        return self.builder.get_object(object_id)

    def exit(self):
        super().exit()
        Gtk.main_quit()

    def get_partidas_options(self):
        partidas = self.con.get_partidas()
        ret = Gtk.ListStore(int, str)

        for partida in partidas:
            logger.debug('Cargando partida id {} nombre {}'.format(
                            partida.id, partida.nombre))
            ret.append([partida.id, partida.nombre])

        return ret

    def load_partidas_combo(self):
        renderer_text = Gtk.CellRendererCombo()

        # cargar combo partida
        partidas_store = self.get_partidas_options()
        combo_partidas = self.builder.get_object("combo-partida")
        combo_partidas.clear()
        combo_partidas.set_model(partidas_store)
        combo_partidas.pack_start(renderer_text, True)
        combo_partidas.add_attribute(renderer_text, "text", 1)

    def load_partida_info(self, partida=None):
        if not partida:
            partida = self.partida

        lab_partida_nombre = self.builder.get_object("label-partida-name")
        tx_partida_descripcion = self.builder.get_object("text-partida-descripcion")

        lab_partida_nombre.set_text(partida.nombre)
        info_buffer = Gtk.TextBuffer()
        descripcion = '' if not partida.descripcion else partida.descripcion
        info_buffer.set_text(descripcion)
        tx_partida_descripcion.set_buffer(info_buffer)

    def tabs_start(self, sensitive):
        tab1 = self.builder.get_object("tab-partida")
        tab1.set_sensitive(sensitive)
        tab2 = self.builder.get_object("tab-equipo")
        tab2.set_sensitive(sensitive)
        tab3 = self.builder.get_object("tab-personaje")
        tab3.set_sensitive(sensitive)
        tab4 = self.builder.get_object("tab-tiradas")
        tab4.set_sensitive(sensitive)
        tab5 = self.builder.get_object("tab-combate")
        tab5.set_sensitive(sensitive)

    def run(self):
        super().run()
        self.build()
        self.bind_signals()
        Gtk.main()


class Handler:
    def onDestroy(self, *args):
        gui = GnGGladeGui.get_instance()
        gui.exit()

    def onShowMain(self, *args):
        gui = GnGGladeGui.get_instance()

        # oscurecer otras pestañas
        gui.tabs_start(False)

        # load partidas combo
        gui.load_partidas_combo()

    def onCrearPartida(self, *args):
        gui = GnGGladeGui.get_instance()
        con = gui.get_controller()

        enewpartida = gui.get_object("entry-partida")
        nombre = enewpartida.get_text()
        logger.debug('Crear partida: {}'.format(nombre))

        con.crear_partida(nombre)

        # reset input
        enewpartida.set_text('')

        # reload partida combo
        gui.load_partidas_combo()

    def onSeleccionarPartida(self, *args):
        gui = GnGGladeGui.get_instance()
        con = gui.get_controller()

        # obtener partida seleccionada
        cselpartida = gui.get_object("combo-partida")
        active_iter = cselpartida.get_active_iter()

        # si no es null, cargar partida y habilitar pestañas
        if active_iter:
            id_partida = cselpartida.get_model()[active_iter][-2]
            logger.debug("Cargando partida id {}".format(id_partida))
            gui.partida = con.get_partida(id_partida)

            gui.tabs_start(True)

            # cargar widgets pestaña partida
            gui.load_partida_info()

    def onBorrarPartida(self, *args):
        gui = GnGGladeGui.get_instance()
        con = gui.get_controller()

        # obtener partida seleccionada
        cselpartida = gui.get_object("combo-partida")
        active_iter = cselpartida.get_active_iter()

        # si no es null, borrar partida, deshabilitar pestañas y recargar combo
        if active_iter:
            id_partida = cselpartida.get_model()[active_iter][-2]
            delpartida = con.get_partida(id_partida)
            current_partida = False
            if delpartida == gui.partida:
                current_partida = True

            logger.debug("Borrando partida id {}".format(id_partida))
            con.borrar_partida(id_partida)
            # comprobar si la partida que hemos borrado es la actual
            if current_partida:
                gui.tabs_start(False)

            gui.load_partidas_combo()

    def onEditPartida(self, *args):
        gui = GnGGladeGui.get_instance()
        con = gui.get_controller()

        # obtener texto
        text_buffer = gui.get_object("text-partida-descripcion")\
                                .get_buffer()
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        new_description = text_buffer.get_text(start, end, False)
        con.editar_partida(gui.partida.id, gui.partida.nombre, new_description)

def run_gui():
    gui = GnGGladeGui.get_instance()
    gui = gui.run()

if __name__ == '__main__':
    run_gui()
