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
    def get_mods_options(self, with_empty=True):
        mods = self.con.get_mods()
        ret = Gtk.ListStore(int, str)

        # iniciar iter list mods equipo
        if with_empty:
            self.eqmod_iters = {}

            # append empty
            empty_iter = ret.append([-1, ''])
            self.eqmod_iters[-1] = empty_iter

        for mod in mods:
            logger.debug('Cargando mod id {} nombre {}'.format(
                            mod.id, mod.nombre))
            new_iter = ret.append([mod.id, mod.nombre])
            if with_empty:
                self.eqmod_iters[mod.id] = new_iter

        return ret

    def load_mods_combo(self):
        # cargar combo partida
        renderer_text = Gtk.CellRendererCombo()
        mods_combos = []
        mods_combos.append((self.builder.get_object("combo-equipo-mod"), True))
        mods_combos.append((self.builder.get_object("combo-mod-tirada"), False))

        for combo, with_empty in mods_combos:
            mods_store = self.get_mods_options(with_empty)
            combo.clear()
            combo.set_model(mods_store)
            combo.pack_start(renderer_text, True)
            combo.add_attribute(renderer_text, "text", 1)

    def get_razas_options(self):
        razas = self.con.get_razas()
        ret = Gtk.ListStore(int, str)

        # iniciar iter list razas pj
        self.pjraza_iters = {}

        for raza in razas:
            logger.debug('Cargando raza id {} nombre {}'.format(
                            raza.id, raza.nombre))
            new_iter = ret.append([raza.id, raza.nombre])
            self.pjraza_iters[raza.id] = new_iter

        return ret

    def load_razas_combo(self):
        # cargar combo partida
        renderer_text = Gtk.CellRendererCombo()
        mods_store = self.get_razas_options()
        combo_mods = self.builder.get_object("combo-personaje-raza")
        combo_mods.clear()
        combo_mods.set_model(mods_store)
        combo_mods.pack_start(renderer_text, True)
        combo_mods.add_attribute(renderer_text, "text", 1)

    def get_equipos_options(self):
        equipos = self.con.get_equipos()
        ret = Gtk.ListStore(int, str)

        # iniciar iter list equipo pj
        self.pjequi_iters = {}

        for equipo in equipos:
            texto_mod = ''
            if equipo.mod:
                if equipo.valor > 0:
                    texto_mod = ' +{} en {}'.format(equipo.valor, equipo.mod.nombre)
                elif equipo.valor < 0:
                    texto_mod = ' {} en {}'.format(equipo.valor, equipo.mod.nombre)

            texto_nombre = '{}{}'.format(
                equipo.nombre,
                texto_mod,
            )
            logger.debug('Cargando equipo id {} nombre {}'.format(
                            equipo.id, texto_nombre))
            new_iter = ret.append([equipo.id, texto_nombre])

        return ret

    def load_equipos_combo(self):
        # cargar combo equipos
        renderer_text = Gtk.CellRendererCombo()
        mods_store = self.get_equipos_options()
        combo_mods = self.builder.get_object("combo-personaje-equipo")
        combo_mods.clear()
        combo_mods.set_model(mods_store)
        combo_mods.pack_start(renderer_text, True)
        combo_mods.add_attribute(renderer_text, "text", 1)

    def get_personajes_options(self):
        personajes = self.con.get_personajes()
        ret = Gtk.ListStore(int, str)

        # iniciar iter list equipo pj
        self.pj_iters = {}

        for personaje in personajes:
            txt_nombre = '{} lu {} : {} : ({})'.format(
                personaje.nombre,
                personaje.profesion,
                personaje.raza.nombre,
                personaje.pueblo,
            )
            logger.debug('Cargando personaje id {} nombre {}'.format(
                            personaje.id, txt_nombre))
            new_iter = ret.append([personaje.id, txt_nombre])

        return ret

    def load_personajes_combos(self):
        # cargar combo equipos
        renderer_text = Gtk.CellRendererCombo()

        combos_pj = []
        combos_pj.append(self.builder.get_object("combo-pj-tirada"))
        combos_pj.append(self.builder.get_object("combo-pnj-tirada"))
        combos_pj.append(self.builder.get_object("combo-pj-combate"))
        combos_pj.append(self.builder.get_object("combo-pnj-combate"))

        for combo in combos_pj:
            pjs_store = self.get_personajes_options()
            combo.clear()
            combo.set_model(pjs_store)
            combo.pack_start(renderer_text, True)
            combo.add_attribute(renderer_text, "text", 1)

    def get_dificultades_options(self):
        dificultades = self.con.get_dificultades()
        ret = Gtk.ListStore(int, str)

        for dificultad in dificultades:
            txt_dificultad = '{} ({})'.format(dificultad.texto, dificultad.valor)
            logger.debug('Cargando dificultad  {}'.format(txt_dificultad))
            new_iter = ret.append([dificultad.id, txt_dificultad])

        return ret

    def load_dificultades_combo(self):
        # cargar combo equipos
        renderer_text = Gtk.CellRendererCombo()
        mods_store = self.get_dificultades_options()
        combo_mods = self.builder.get_object("combo-dificultad-tirada")
        combo_mods.clear()
        combo_mods.set_model(mods_store)
        combo_mods.pack_start(renderer_text, True)
        combo_mods.add_attribute(renderer_text, "text", 1)

    def load_spiners(self):
        # get spinners
        equipo_valor = self.get_object("spin-equipo-valor")
        pj_hp = self.get_object("spinner-personaje-hp")
        pj_fuerza = self.get_object("spinner-personaje-fuerza")
        pj_agilidad = self.get_object("spinner-personaje-agilidad")
        pj_inteligencia = self.get_object("spinner-personaje-inteligencia")
        pj_carisma = self.get_object("spinner-personaje-carisma")
        pj_combate = self.get_object("spinner-personaje-combate")
        pj_conocimientos = self.get_object("spinner-personaje-conocimientos")
        pj_latrocinio = self.get_object("spinner-personaje-latrocinio")
        pj_magia = self.get_object("spinner-personaje-magia")
        pj_sociales = self.get_object("spinner-personaje-sociales")
        bonuspj_tirada = self.get_object("spinner-bonuspj-tirada")
        bonuspnj_tirada = self.get_object("spinner-bonuspnj-tirada")

        skill_spiners = [pj_fuerza, pj_agilidad, pj_inteligencia,
                            pj_inteligencia, pj_carisma, pj_combate,
                            pj_conocimientos, pj_latrocinio, pj_magia,
                            pj_sociales]
        all_spiners = [pj_hp, equipo_valor, bonuspj_tirada, bonuspnj_tirada
                        ]\
                        + skill_spiners

        # set all to integer spinners
        for spiner in all_spiners:
            spiner.set_digits(0)
            spiner.set_numeric(True)

        # set adjustements
        for spiner in all_spiners:
            spiner.set_adjustment(Gtk.Adjustment(0, -1000, 1000, 1, 0, 0))

        for spiner in skill_spiners:
            spiner.set_adjustment(Gtk.Adjustment(0, 1, 8, 1, 0, 0))

        pj_hp.set_adjustment(Gtk.Adjustment(0, 0, 1000, 1, 0, 0))

    def build(self):
        # build glade
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui/gngui.glade")

        # cargar combos
        self.load_partidas_combo()
        self.load_mods_combo()
        self.load_razas_combo()
        self.load_equipos_combo()
        self.load_dificultades_combo()
        self.load_spiners()

        # cargar lista equipo
        self.load_list_equipo()

        # set vars
        self.id_personaje_sel = None

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

        ## tab personajes ##
        bguardarpj = self.builder.get_object("button-personaje-guardar")
        bguardarpj.connect("clicked", Handler.onGuardarPersonajeButton)

        ## tab tiradas ##
        btirarso = self.builder.get_object("button-tirarso-tiradas")
        btirarso.connect("clicked", Handler.onTirarSinOposicion)

        bborrarso = self.builder.get_object("button-borrarso-tiradas")
        bborrarso.connect("clicked", Handler.onBorrarSinOposicion)

        btirarco = self.builder.get_object("button-tirarco-tiradas")
        btirarco.connect("clicked", Handler.onTirarConOposicion)

        bborrarco = self.builder.get_object("button-borrarco-tiradas")
        bborrarco.connect("clicked", Handler.onBorrarConOposicion)

        self.bt_asignar_activado = False

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

    def load_list_equipo(self):
        list_equipo = self.get_object("equipos-list")
        equipos = self.con.get_equipos()

        for equipo in equipos:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            row.add(hbox)

            texto_mod = ''
            if equipo.mod:
                if equipo.valor > 0:
                    texto_mod = ' +{} en {}'.format(equipo.valor, equipo.mod.nombre)
                elif equipo.valor < 0:
                    texto_mod = ' {} en {}'.format(equipo.valor, equipo.mod.nombre)

            texto_nombre = '{}{}'.format(
                equipo.nombre,
                texto_mod,
            )
            label_datos = Gtk.Label(texto_nombre, xalign=0)
            hbox.pack_start(label_datos, True, True, 0)

            label_descrip = Gtk.Label(equipo.descripcion, xalign=0)
            hbox.pack_start(label_descrip, True, True, 0)

            button_editar = Gtk.Button.new_with_label("Editar")
            button_editar.connect('clicked', Handler.onEditarEquipoButton, {'id_equipo': equipo.id})
            hbox.pack_start(button_editar, True, True, 0)

            button_borrar = Gtk.Button.new_with_label("Borrar")
            button_borrar.connect('clicked', Handler.onBorrarEquipoButton, {'id_equipo': equipo.id})
            hbox.pack_start(button_borrar, True, True, 0)

            list_equipo.add(row)

        list_equipo.show_all()

    def refrescar_lista_equipo(self):
        logger.debug('Refrescando lista equipo')
        list_equipo = self.get_object("equipos-list")
        children = list_equipo.get_children()
        for child in children:
            list_equipo.remove(child)

        self.load_list_equipo()

    def load_list_personajes(self):
        list_personaje = self.get_object("list-personajes")
        personajes = self.con.get_personajes(self.partida.id)

        for personaje in personajes:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            row.add(hbox)

            txt_nombre = '{} lu {} : {} : ({})'.format(
                personaje.nombre,
                personaje.profesion,
                personaje.raza.nombre,
                personaje.pueblo,
            )
            label_nombre = Gtk.Label(txt_nombre, xalign=0)
            hbox.pack_start(label_nombre, True, True, 0)

            txt_stats = 'HP{} FU{} AG{} IN{} CA{} CO{} CN{} LA{} MA{} SO{}'.format(
                personaje.hp,
                personaje.fuerza,
                personaje.agilidad,
                personaje.inteligencia,
                personaje.carisma,
                personaje.combate,
                personaje.conocimientos,
                personaje.latrocinio,
                personaje.magia,
                personaje.sociales,
            )
            label_stats = Gtk.Label(txt_stats, xalign=0)
            hbox.pack_start(label_stats, True, True, 0)

            button_editar = Gtk.Button.new_with_label("Editar")
            button_editar.connect('clicked', Handler.onEditarPersonajeButton, {'id_personaje': personaje.id})
            hbox.pack_start(button_editar, True, True, 0)

            button_borrar = Gtk.Button.new_with_label("Borrar")
            button_borrar.connect('clicked', Handler.onBorrarPersonajeButton, {'id_personaje': personaje.id})
            hbox.pack_start(button_borrar, True, True, 0)

            list_personaje.add(row)

        list_personaje.show_all()

    def refrescar_lista_personajes(self):
        logger.debug('Refrescando lista personajes')
        list_personajes = self.get_object("list-personajes")
        children = list_personajes.get_children()
        for child in children:
            list_personajes.remove(child)

        self.load_list_personajes()

    def load_list_equipos_pj(self):
        self.refrescar_lista_equipos_pj(True)
        list_equipo = self.get_object("list-personaje-equipo")

        if self.id_personaje_sel:
            equipos = self.con.get_equipos_personaje(self.id_personaje_sel)

            for equipo in equipos:
                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)

                texto_mod = ''
                if equipo.mod:
                    if equipo.valor > 0:
                        texto_mod = ' +{} en {}'.format(equipo.valor, equipo.mod.nombre)
                    elif equipo.valor < 0:
                        texto_mod = ' {} en {}'.format(equipo.valor, equipo.mod.nombre)

                texto_nombre = '{}{}'.format(
                    equipo.nombre,
                    texto_mod,
                )
                label_datos = Gtk.Label(texto_nombre, xalign=0)
                hbox.pack_start(label_datos, True, True, 0)

                label_descrip = Gtk.Label(equipo.descripcion, xalign=0)
                hbox.pack_start(label_descrip, True, True, 0)

                button_borrar = Gtk.Button.new_with_label("Borrar")
                button_borrar.connect('clicked', Handler.onBorrarEquipoPjButton, {'id_pj_equipo': equipo.id_pj_equipo})
                hbox.pack_start(button_borrar, True, True, 0)

                list_equipo.add(row)

            list_equipo.show_all()

    def refrescar_lista_equipos_pj(self, delete=False):
        logger.debug('Refrescando lista equipos asignados')
        list_equipo = self.get_object("list-personaje-equipo")
        children = list_equipo.get_children()
        for child in children:
            list_equipo.remove(child)

        if not delete:
            self.load_list_equipos_pj()

    def limpiar_form_personaje(self):
        entry_nombre = self.get_object("entry-personaje-nombre")
        entry_profesion = self.get_object("entry-personaje-profesion")
        combo_raza = self.get_object("combo-personaje-raza")
        entry_pueblo = self.get_object("entry-personaje-pueblo")
        spinner_hp = self.get_object("spinner-personaje-hp")
        spinner_fuerza = self.get_object("spinner-personaje-fuerza")
        spinner_agilidad = self.get_object("spinner-personaje-agilidad")
        spinner_inteligencia = self.get_object("spinner-personaje-inteligencia")
        spinner_carisma = self.get_object("spinner-personaje-carisma")
        spinner_combate = self.get_object("spinner-personaje-combate")
        spinner_conocimientos = self.get_object("spinner-personaje-conocimientos")
        spinner_latrocinio = self.get_object("spinner-personaje-latrocinio")
        spinner_magia = self.get_object("spinner-personaje-magia")
        spinner_sociales = self.get_object("spinner-personaje-sociales")
        text_notas = self.get_object("text-personaje-notas")
        button_asignar = self.get_object("button-personaje-equipo")
        label_ataque = self.get_object("label-personaje-ataque")
        label_defensa = self.get_object("label-personaje-defensa")

        entry_nombre.set_text('')
        entry_profesion.set_text('')
        entry_pueblo.set_text('')
        text_notas.set_buffer(Gtk.TextBuffer())
        spinner_hp.set_value(1)
        spinner_fuerza.set_value(1)
        spinner_agilidad.set_value(1)
        spinner_inteligencia.set_value(1)
        spinner_carisma.set_value(1)
        spinner_combate.set_value(1)
        spinner_conocimientos.set_value(1)
        spinner_latrocinio.set_value(1)
        spinner_magia.set_value(1)
        spinner_sociales.set_value(1)
        combo_raza.set_active_iter(None)
        label_ataque.set_text('_')
        label_defensa.set_text('_')

        button_asignar.set_sensitive(False)
        button_asignar.connect("clicked", Handler.voidCallback)
        self.bt_asignar_activado = False
        self.refrescar_lista_equipos_pj(True)

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
            gui.load_list_personajes()
            gui.limpiar_form_personaje()
            gui.load_personajes_combos()

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

        is_create = False

        if not hasattr(gui, 'id_equipo_sel'):
            is_create = True
        elif not gui.id_equipo_sel:
            is_create = True

        if is_create:
            # create
            logger.debug('''Crear equipo: nombre {} / descripcion {} / id_mod {} / valor {}
            '''.format(nombre, descripcion, id_mod, valor))
            con.crear_equipo(nombre, descripcion, valor, id_mod)
        else:
            # edit
            logger.debug('''Editar equipo: nombre {} / descripcion {} / id_mod {} / valor {}
            '''.format(nombre, descripcion, id_mod, valor))
            con.editar_equipo(gui.id_equipo_sel, nombre, descripcion, valor, id_mod)
            gui.id_equipo_sel = None

        gui.limpiar_form_equipo()
        gui.refrescar_lista_equipo()
        gui.load_equipos_combo()
        gui.refrescar_lista_equipos_pj()

    def onEditarEquipoButton(self, *args):
        gui, con = get_utils()

        # cargar valores en formulario
        entry_nombre = gui.get_object("entry-equipo-nombre")
        combo_mod = gui.get_object("combo-equipo-mod")
        spin_valor = gui.get_object("spin-equipo-valor")
        equipo_descripcion = gui.get_object("equipo-text-descripcion")

        equipo = con.get_equipo(args[0]['id_equipo'])

        entry_nombre.set_text(equipo.nombre)
        new_buffer = Gtk.TextBuffer()
        new_buffer.set_text(equipo.descripcion)
        equipo_descripcion.set_buffer(new_buffer)
        spin_valor.set_value(equipo.valor)
        # get active iter
        active_iter = gui.eqmod_iters[equipo.mod.id]
        combo_mod.set_active_iter(active_iter)

        # setear id_equipo_sel
        gui.id_equipo_sel = equipo.id

    def onBorrarEquipoButton(self, *args):
        gui, con = get_utils()
        id_equipo = args[0]['id_equipo']
        logger.debug('Borrando equipo con id {}'.format(id_equipo))
        con.borrar_equipo(id_equipo)
        gui.refrescar_lista_equipo()
        gui.load_equipos_combo()
        gui.refrescar_lista_equipos_pj()

    def onGuardarPersonajeButton(self, *args):
        gui, con = get_utils()
        entry_nombre = gui.get_object("entry-personaje-nombre")
        entry_profesion = gui.get_object("entry-personaje-profesion")
        combo_raza = gui.get_object("combo-personaje-raza")
        entry_pueblo = gui.get_object("entry-personaje-pueblo")
        spinner_hp = gui.get_object("spinner-personaje-hp")
        spinner_fuerza = gui.get_object("spinner-personaje-fuerza")
        spinner_agilidad = gui.get_object("spinner-personaje-agilidad")
        spinner_inteligencia = gui.get_object("spinner-personaje-inteligencia")
        spinner_carisma = gui.get_object("spinner-personaje-carisma")
        spinner_combate = gui.get_object("spinner-personaje-combate")
        spinner_conocimientos = gui.get_object("spinner-personaje-conocimientos")
        spinner_latrocinio = gui.get_object("spinner-personaje-latrocinio")
        spinner_magia = gui.get_object("spinner-personaje-magia")
        spinner_sociales = gui.get_object("spinner-personaje-sociales")
        text_notas = gui.get_object("text-personaje-notas")

        ## llenando data
        data = {}
        # entries
        data['nombre'] = entry_nombre.get_text()
        data['profesion'] = entry_profesion.get_text()
        data['pueblo'] = entry_pueblo.get_text()
        # combo
        data['raza'] = 0

        raza_active_iter = combo_raza.get_active_iter()
        if raza_active_iter:
            data['raza'] = combo_raza.get_model()[raza_active_iter][-2]
        # spinners
        data['hp'] = spinner_hp.get_value_as_int()
        data['fuerza'] = spinner_fuerza.get_value_as_int()
        data['agilidad'] = spinner_agilidad.get_value_as_int()
        data['inteligencia'] = spinner_inteligencia.get_value_as_int()
        data['carisma'] = spinner_carisma.get_value_as_int()
        data['combate'] = spinner_combate.get_value_as_int()
        data['conocimientos'] = spinner_conocimientos.get_value_as_int()
        data['latrocinio'] = spinner_latrocinio.get_value_as_int()
        data['magia'] = spinner_magia.get_value_as_int()
        data['sociales'] = spinner_sociales.get_value_as_int()
        data['partida'] = gui.partida.id

        # notas
        data['notas'] = text_notas.get_buffer().get_text(
            text_notas.get_buffer().get_start_iter(),
            text_notas.get_buffer().get_end_iter(),
            False
        )

        is_create = False

        if not hasattr(gui, 'id_personaje_sel'):
            is_create = True
        elif not gui.id_personaje_sel:
            is_create = True

        if is_create:
            logger.debug('Crear personaje:')
            logger.debug(data)
            con.crear_personaje(data)
        else:
            logger.debug('Editar personaje')
            logger.debug(data)
            con.editar_personaje(gui.id_personaje_sel, data)
            gui.id_personaje_sel = None

        gui.limpiar_form_personaje()
        gui.refrescar_lista_personajes()
        gui.load_personajes_combos()

    @classmethod
    def cargarLabelsAtaqueDefensa(cls):
        gui, con = get_utils()
        label_ataque = gui.get_object("label-personaje-ataque")
        label_defensa = gui.get_object("label-personaje-defensa")

        # calcular ataque y defensa (a lo cazurro)
        personaje = con.get_personaje(gui.id_personaje_sel)
        equipos = con.get_equipos_personaje(personaje.id)
        mods = con.get_mods()
        mod_ataque, mod_defensa = None, None
        for mod in mods:
            if mod.nombre == 'Ataque':
                mod_ataque = mod
            if mod.nombre == 'Defensa':
                mod_defensa = mod

        bonus_ataque = con.bonus_equipo_personaje(mod_ataque, personaje)
        bonus_defensa = con.bonus_equipo_personaje(mod_defensa, personaje)

        ataque  = personaje.combate + bonus_ataque
        defensa = personaje.combate + bonus_defensa

        label_ataque.set_text(str(ataque))
        label_defensa.set_text(str(defensa))

    def onEditarPersonajeButton(self, *args):
        gui, con = get_utils()

        # cargar valores en formulario
        entry_nombre = gui.get_object("entry-personaje-nombre")
        entry_profesion = gui.get_object("entry-personaje-profesion")
        combo_raza = gui.get_object("combo-personaje-raza")
        entry_pueblo = gui.get_object("entry-personaje-pueblo")
        spinner_hp = gui.get_object("spinner-personaje-hp")
        spinner_fuerza = gui.get_object("spinner-personaje-fuerza")
        spinner_agilidad = gui.get_object("spinner-personaje-agilidad")
        spinner_inteligencia = gui.get_object("spinner-personaje-inteligencia")
        spinner_carisma = gui.get_object("spinner-personaje-carisma")
        spinner_combate = gui.get_object("spinner-personaje-combate")
        spinner_conocimientos = gui.get_object("spinner-personaje-conocimientos")
        spinner_latrocinio = gui.get_object("spinner-personaje-latrocinio")
        spinner_magia = gui.get_object("spinner-personaje-magia")
        spinner_sociales = gui.get_object("spinner-personaje-sociales")
        text_notas = gui.get_object("text-personaje-notas")

        personaje = con.get_personaje(args[0]['id_personaje'])

        entry_nombre.set_text(personaje.nombre)
        entry_profesion.set_text(personaje.profesion)
        entry_pueblo.set_text(personaje.pueblo)
        new_buffer = Gtk.TextBuffer()
        new_buffer.set_text(personaje.notas)
        text_notas.set_buffer(new_buffer)
        spinner_hp.set_value(personaje.hp)
        spinner_fuerza.set_value(personaje.fuerza)
        spinner_agilidad.set_value(personaje.agilidad)
        spinner_inteligencia.set_value(personaje.inteligencia)
        spinner_carisma.set_value(personaje.carisma)
        spinner_combate.set_value(personaje.combate)
        spinner_conocimientos.set_value(personaje.conocimientos)
        spinner_latrocinio.set_value(personaje.latrocinio)
        spinner_magia.set_value(personaje.magia)
        spinner_sociales.set_value(personaje.sociales)
        # get active iter
        active_iter = gui.pjraza_iters[personaje.raza.id]
        combo_raza.set_active_iter(active_iter)

        # activar botón asignar equipo
        button_asignar = gui.get_object("button-personaje-equipo")
        button_asignar.set_sensitive(True)
        if not gui.bt_asignar_activado:
            gui.bt_asignar_activado = True
            button_asignar.connect("clicked", Handler.onAsignarEquipo)

        # setear id_personaje_sel
        gui.id_personaje_sel = personaje.id
        gui.load_list_equipos_pj()
        Handler.cargarLabelsAtaqueDefensa()

    def onBorrarPersonajeButton(self, *args):
        gui, con = get_utils()
        id_personaje = args[0]['id_personaje']
        logger.debug('Borrando personaje con id {}'.format(id_personaje))
        con.borrar_personaje(id_personaje)
        gui.refrescar_lista_personajes()
        gui.load_personajes_combos()

    def onAsignarEquipo(self, *args):
        gui, con = get_utils()
        # obtener partida seleccionada
        combo_equipo = gui.get_object("combo-personaje-equipo")
        active_iter = combo_equipo.get_active_iter()

        # si no es null, cargar partida y habilitar pestañas
        if active_iter:
            id_equipo = combo_equipo.get_model()[active_iter][-2]
            logger.debug("Asignando equipo id {} a pj {}".format(id_equipo, gui.id_personaje_sel))
            con.asignar_equipo(gui.id_personaje_sel, id_equipo)
            gui.refrescar_lista_equipos_pj()
            Handler.cargarLabelsAtaqueDefensa()

    def onBorrarEquipoPjButton(self, *args):
        gui, con = get_utils()
        id_pj_equipo = args[0]['id_pj_equipo']
        logger.debug('Desasignando equipo con id {}'.format(id_pj_equipo))
        con.desasignar_equipo(id_pj_equipo)
        gui.refrescar_lista_equipos_pj()
        Handler.cargarLabelsAtaqueDefensa()

    def onTirarSinOposicion(self, *args):
        gui, con = get_utils()

        # obtener personaje
        cpjtirada = gui.get_object("combo-pj-tirada")
        cpjtirada_ai = cpjtirada.get_active_iter()

        # obtener mod
        cmodtirada = gui.get_object("combo-mod-tirada")
        cmodtirada_ai = cmodtirada.get_active_iter()

        # obtener dificultad
        cdiftirada = gui.get_object("combo-dificultad-tirada")
        cdiftirada_ai = cdiftirada.get_active_iter()

        # obtener valor bonus
        spbonuspj = gui.get_object("spinner-bonuspj-tirada")
        bonus = spbonuspj.get_value_as_int()

        # tirar
        if cpjtirada_ai and cmodtirada_ai and cdiftirada_ai:
            id_personaje = cpjtirada.get_model()[cpjtirada_ai][-2]
            id_mod = cmodtirada.get_model()[cmodtirada_ai][-2]
            id_dificultad = cdiftirada.get_model()[cdiftirada_ai][-2]

            res = con.tirada_sin_oposicion(
                id_personaje, id_dificultad, id_mod, bonus
            )

            cuenta = res['pjvalue'] + res['dado'] + res['equipo_bonus'] + bonus

            # formatear texto tirada
            txt_tirada = 'S{}+[{}]+E{}+B{} = {} > D{}'.format(
                res['pjvalue'],
                res['dado'],
                res['equipo_bonus'],
                bonus,
                cuenta,
                res['dif'],
            )

            # formatear texto resultado
            txt_resultado = 'OK' if res['resultado'] else 'KO'

            # mostrar texto
            label_tirada = gui.get_object("label-tirso-tirada")
            label_resultado = gui.get_object("label-resso-tirada")
            label_tirada.set_text(txt_tirada)
            label_resultado.set_text(txt_resultado)

    def onBorrarSinOposicion(self, *args):
        gui, con = get_utils()

        label_tirada = gui.get_object("label-tirso-tirada")
        label_resultado = gui.get_object("label-resso-tirada")
        label_tirada.set_text('')
        label_resultado.set_text('')

    def onTirarConOposicion(self, *args):
        gui, con = get_utils()

        # obtener personaje
        cpjtirada = gui.get_object("combo-pj-tirada")
        cpjtirada_ai = cpjtirada.get_active_iter()

        # obtener mod
        cmodtirada = gui.get_object("combo-mod-tirada")
        cmodtirada_ai = cmodtirada.get_active_iter()

        # obtener pnj
        cpnjtirada = gui.get_object("combo-pnj-tirada")
        cpnjtirada_ai = cpnjtirada.get_active_iter()

        # obtener valor bonus pj
        spbonuspj = gui.get_object("spinner-bonuspj-tirada")
        bonus_pj = spbonuspj.get_value_as_int()

        # obtener valor bonus pnj
        spbonuspnj = gui.get_object("spinner-bonuspnj-tirada")
        bonus_pnj = spbonuspnj.get_value_as_int()

        # tirar
        if cpjtirada_ai and cmodtirada_ai and cpnjtirada:
            id_personaje = cpjtirada.get_model()[cpjtirada_ai][-2]
            id_pnj = cpnjtirada.get_model()[cpnjtirada_ai][-2]
            id_mod = cmodtirada.get_model()[cmodtirada_ai][-2]

            res = con.tirada_con_oposicion(
                id_personaje,
                id_pnj,
                id_mod,
                bonus_pj,
                bonus_pnj
            )

            cuenta_pj = res['pjvalue'] + res['dado1'] + res['equipo_bonus_pj1'] + bonus_pj
            cuenta_pnj = res['pnjvalue'] + res['dado2'] + res['equipo_bonus_pnj'] + bonus_pj
            symbol = '>' if res['resultado'] else '<'

            # formatear texto tirada
            txt_tirada = 'S{}+[{}]+E{}+B{} = {} {} {} = S{}+[{}]+E{}+B{}'.format(
                res['pjvalue'],
                res['dado1'],
                res['equipo_bonus_pj1'],
                bonus_pj,
                cuenta_pj,
                symbol,
                cuenta_pnj,
                res['pnjvalue'],
                res['dado2'],
                res['equipo_bonus_pnj'],
                bonus_pnj,
            )

            # formatear texto resultado
            txt_resultado = 'PJ GANA' if res['resultado'] else 'PJ PIERDE'

            # mostrar texto
            label_tirada = gui.get_object("label-tirco-tirada")
            label_resultado = gui.get_object("label-resco-tirada")
            label_tirada.set_text(txt_tirada)
            label_resultado.set_text(txt_resultado)

    def onBorrarConOposicion(self, *args):
        gui, con = get_utils()
        label_tirada = gui.get_object("label-tirco-tirada")
        label_resultado = gui.get_object("label-resco-tirada")
        label_tirada.set_text('')
        label_resultado.set_text('')

    def voidCallback(self, *args):
        pass


def run_gui():
    gui = GnGGladeGui.get_instance()
    gui = gui.run()

if __name__ == '__main__':
    run_gui()
