from . import *

class CrudPersonajeTest(BaseConDatosGtkGui):
    def rellenar_pj_guardar(self, pj_vars):
        # controles
        entry_nombre = self.gui.builder.get_object("entry-personaje-nombre")
        entry_profesion = self.gui.builder.get_object("entry-personaje-profesion")
        entry_pueblo = self.gui.builder.get_object("entry-personaje-pueblo")
        combo_raza = self.gui.get_object("combo-personaje-raza")
        bt_resethp = self.gui.builder.get_object("button-personaje-resethp")

        spin_fuerza = self.gui.builder.get_object("spinner-personaje-fuerza")
        spin_agilidad = self.gui.builder.get_object("spinner-personaje-agilidad")
        spin_inteligencia = self.gui.builder.get_object("spinner-personaje-inteligencia")
        spin_carisma = self.gui.builder.get_object("spinner-personaje-carisma")

        spin_combate = self.gui.builder.get_object("spinner-personaje-combate")
        spin_conocimientos = self.gui.builder.get_object("spinner-personaje-conocimientos")
        spin_latrocinio = self.gui.builder.get_object("spinner-personaje-latrocinio")
        spin_magia = self.gui.builder.get_object("spinner-personaje-magia")
        spin_sociales = self.gui.builder.get_object("spinner-personaje-sociales")

        text_notas = self.gui.builder.get_object("text-personaje-notas")
        bt_guardar = self.gui.builder.get_object("button-personaje-guardar")

        # rellenar
        entry_nombre.set_text(pj_vars['nombre'])
        entry_profesion.set_text(pj_vars['profesion'])
        entry_pueblo.set_text(pj_vars['pueblo'])

        active_iter = self.gui.pjraza_iters[pj_vars['raza'].id]
        combo_raza.set_active_iter(active_iter)

        spin_fuerza.set_value(pj_vars['fuerza'])
        spin_agilidad.set_value(pj_vars['agilidad'])
        spin_inteligencia.set_value(pj_vars['inteligencia'])
        spin_carisma.set_value(pj_vars['carisma'])

        spin_combate.set_value(pj_vars['combate'])
        spin_conocimientos.set_value(pj_vars['conocimientos'])
        spin_latrocinio.set_value(pj_vars['latrocinio'])
        spin_magia.set_value(pj_vars['magia'])
        spin_sociales.set_value(pj_vars['sociales'])

        info_buffer = Gtk.TextBuffer()
        info_buffer.set_text(pj_vars['notas'])
        text_notas.set_buffer(info_buffer)

        refresh_gui()

        # resetear hp para rellenarla a valor por defecto
        bt_resethp.clicked()
        refresh_gui()

        # guardar
        bt_guardar.clicked()
        refresh_gui()

    def comparar_pj_datos(self, personaje, pj_vars):
        self.assertEqual(personaje.nombre, pj_vars['nombre'])
        self.assertEqual(personaje.profesion, pj_vars['profesion'])
        self.assertEqual(personaje.raza, pj_vars['raza'])
        self.assertEqual(personaje.pueblo, pj_vars['pueblo'])
        self.assertEqual(personaje.hp, pj_vars['hp'])

        self.assertEqual(personaje.fuerza, pj_vars['fuerza'])
        self.assertEqual(personaje.agilidad, pj_vars['agilidad'])
        self.assertEqual(personaje.inteligencia, pj_vars['inteligencia'])
        self.assertEqual(personaje.carisma, pj_vars['carisma'])

        self.assertEqual(personaje.combate, pj_vars['combate'])
        self.assertEqual(personaje.conocimientos, pj_vars['conocimientos'])
        self.assertEqual(personaje.latrocinio, pj_vars['latrocinio'])
        self.assertEqual(personaje.magia, pj_vars['magia'])
        self.assertEqual(personaje.sociales, pj_vars['sociales'])

        self.assertEqual(personaje.notas, pj_vars['notas'])
        self.assertEqual(personaje.is_pj, pj_vars['is_pj'])

    def test_cud_personaje(self):
        self.seleccionar_partida()

        # crear presonaje
        # variables personaje
        pj_vars = self.db_creator.generar_personaje()
        self.rellenar_pj_guardar(pj_vars)

        # comprobar personaje en base de datos
        partida_db = self.con.get_partidas()[0]
        personajes_partida = self.con.get_personajes(partida_db.id)
        personaje = personajes_partida[-1]

        self.comparar_pj_datos(personaje, pj_vars)
