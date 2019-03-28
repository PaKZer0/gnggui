import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import logging
from pprint import pprint

from core.controller import Controller
from gui.abstractgui import AbstractGui

logger = logging.getLogger(__name__)

def get_utils():
    gui = GnGGladeGui.get_instance()
    con = gui.get_controller()

    return gui, con

class GnGGladeGui(AbstractGui):
    def get_mods_options(self):
        mods = self.con.get_mods()
        ret = Gtk.ListStore(int, str)

        # append empty
        ret.append([-1, ''])

        for mod in mods:
            logger.debug('Cargando partida id {} nombre {}'.format(
                            mod.id, mod.nombre))
            ret.append([mod.id, mod.nombre])

        return ret

    def load_mods_combo(self):
        # cargar combo partida
        renderer_text = Gtk.CellRendererCombo()
        mods_store = self.get_mods_options()
        combo_mods = self.builder.get_object("combo-equipo-mod")
        combo_mods.clear()
        combo_mods.set_model(mods_store)
        combo_mods.pack_start(renderer_text, True)
        combo_mods.add_attribute(renderer_text, "text", 1)

    def load_spiners(self):
        # get spinners
        equipo_valor = self.get_object("spin-equipo-valor")

        all_spiners = [equipo_valor]
        skill_spiners = []

        unlimited_adjustment = Gtk.Adjustment(0, -100, 100, 1, 0, 0)
        limited_adjustment   = None

        # set all to integer spinners
        for spiner in all_spiners:
            spiner.set_digits(0)
            spiner.set_numeric(True)

        # set rango al spiner de equipo
        equipo_valor.set_adjustment(unlimited_adjustment)

    def build(self):
        # build glade
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui/gngui.glade")

        # cargar mods
        self.load_mods_combo()
        self.load_spiners()

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

        ## tab equipo ##
        bguardarequ = self.builder.get_object("button-equipo-guardar")
        bguardarequ.connect("clicked", Handler.onGuardarEquipo)

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
        # cargar combo partida
        renderer_text = Gtk.CellRendererCombo()
        partidas_store = self.get_partidas_options()
        combo_partidas = self.builder.get_object("combo-partida")
        combo_partidas.clear()
        combo_partidas.set_model(partidas_store)
        combo_partidas.pack_start(renderer_text, True)
        combo_partidas.add_attribute(renderer_text, "text", 1)

    def load_partida_info(self, partida=None):
        if not partida:
            partida = self.partida

        lab_partida_nombre = self.builder.get_object("entry-partida-name")
        tx_partida_descripcion = self.builder.get_object("text-partida-descripcion")

        lab_partida_nombre.set_text(partida.nombre)
        info_buffer = Gtk.TextBuffer()
        descripcion = '' if not partida.descripcion else partida.descripcion
        info_buffer.set_text(descripcion)
        tx_partida_descripcion.set_buffer(info_buffer)

    def limpiar_form_equipo(self):
        entry_nombre = self.get_object("entry-equipo-nombre")
        combo_mod = self.get_object("combo-equipo-mod")
        spin_valor = self.get_object("spin-equipo-valor")
        equipo_descripcion = self.get_object("equipo-text-descripcion")

        entry_nombre.set_text('')
        equipo_descripcion.set_buffer(Gtk.TextBuffer())
        spin_valor.set_value(0)
        combo_mod.set_active_iter(None)

    def cargar_form_equipo(self, id_equipo):
        self.id_equipo_sel = id_equipo

    def cargar_list_equipo(self):
        pass

    def tabs_start(self, sensitive):
        tab1 = self.builder.get_object("tab-partida")
        tab1.set_sensitive(sensitive)
        tab2 = self.builder.get_object("tab-equipo")
        #tab2.set_sensitive(sensitive)
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
        gui, con = get_utils()
        gui.exit()

    def onShowMain(self, *args):
        gui, con = get_utils()
        # oscurecer otras pestañas
        gui.tabs_start(False)

        # load partidas combo
        gui.load_partidas_combo()

    def onCrearPartida(self, *args):
        gui, con = get_utils()
        enewpartida = gui.get_object("entry-partida")
        nombre = enewpartida.get_text()
        logger.debug('Crear partida: {}'.format(nombre))

        con.crear_partida(nombre)

        # reset input
        enewpartida.set_text('')

        # reload partida combo
        gui.load_partidas_combo()

    def onSeleccionarPartida(self, *args):
        gui, con = get_utils()
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
        gui, con = get_utils()
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
        gui, con = get_utils()
        # obtener texto
        text_buffer = gui.get_object("text-partida-descripcion")\
                                .get_buffer()
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        new_description = text_buffer.get_text(start, end, False)

        # obtener nombre
        entry_partida_nombre = gui.builder.get_object("entry-partida-name")
        new_nombre = entry_partida_nombre.get_text()

        con.editar_partida(gui.partida.id, new_nombre, new_description)
        gui.load_partidas_combo()

    def onGuardarEquipo(self, *args):
        gui, con = get_utils()
        entry_nombre = gui.get_object("entry-equipo-nombre")
        combo_mod = gui.get_object("combo-equipo-mod")
        spin_valor = gui.get_object("spin-equipo-valor")
        equipo_descripcion = gui.get_object("equipo-text-descripcion")

        nombre = entry_nombre.get_text()
        descripcion = equipo_descripcion.get_buffer().get_text(
            equipo_descripcion.get_buffer().get_start_iter(),
            equipo_descripcion.get_buffer().get_end_iter(),
            False
        )
        id_mod = 0
        valor = spin_valor.get_value_as_int()

        mod_active_iter = combo_mod.get_active_iter()
        if mod_active_iter:
            id_mod = combo_mod.get_model()[mod_active_iter][-2]

        if not hasattr(gui, 'id_equipo_sel'):
            # create
            logger.warn('''Crear equipo: nombre {} / descripcion {} / id_mod {} / valor {}
            '''.format(nombre, descripcion, id_mod, valor))
            con.crear_equipo(nombre, descripcion, id_mod, valor)
        else:
            pass
            # edit

        gui.limpiar_form_equipo()
        gui.cargar_list_equipo()


def run_gui():
    gui = GnGGladeGui.get_instance()
    gui = gui.run()

if __name__ == '__main__':
    run_gui()
