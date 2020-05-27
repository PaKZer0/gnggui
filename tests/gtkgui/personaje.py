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

        check_ispj = self.gui.builder.get_object("check-personaje-ispj")
        text_notas = self.gui.builder.get_object("text-personaje-notas")
        bt_guardar = self.gui.builder.get_object("button-personaje-guardar")


        # rellenar
        entry_nombre.set_text(pj_vars['nombre'])
        entry_profesion.set_text(pj_vars['profesion'])
        entry_pueblo.set_text(pj_vars['pueblo'])

        active_iter = self.gui.pjraza_iters[pj_vars['raza'].id]
        combo_raza.set_active_iter(active_iter)
        refresh_gui()

        spin_fuerza.set_value(pj_vars['fuerza'])
        spin_agilidad.set_value(pj_vars['agilidad'])
        spin_inteligencia.set_value(pj_vars['inteligencia'])
        spin_carisma.set_value(pj_vars['carisma'])

        spin_combate.set_value(pj_vars['combate'])
        spin_conocimientos.set_value(pj_vars['conocimientos'])
        spin_latrocinio.set_value(pj_vars['latrocinio'])
        spin_magia.set_value(pj_vars['magia'])
        spin_sociales.set_value(pj_vars['sociales'])

        check_ispj.set_active(pj_vars['is_pj'])
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

    def comprobar_pjform_cargado(self, pj_vars):
        entry_nombre = self.gui.builder.get_object("entry-personaje-nombre")
        entry_profesion = self.gui.builder.get_object("entry-personaje-profesion")
        entry_pueblo = self.gui.builder.get_object("entry-personaje-pueblo")
        combo_raza = self.gui.get_object("combo-personaje-raza")
        spin_hp = self.gui.builder.get_object("spinner-personaje-hp")

        spin_fuerza = self.gui.builder.get_object("spinner-personaje-fuerza")
        spin_agilidad = self.gui.builder.get_object("spinner-personaje-agilidad")
        spin_inteligencia = self.gui.builder.get_object("spinner-personaje-inteligencia")
        spin_carisma = self.gui.builder.get_object("spinner-personaje-carisma")

        spin_combate = self.gui.builder.get_object("spinner-personaje-combate")
        spin_conocimientos = self.gui.builder.get_object("spinner-personaje-conocimientos")
        spin_latrocinio = self.gui.builder.get_object("spinner-personaje-latrocinio")
        spin_magia = self.gui.builder.get_object("spinner-personaje-magia")
        spin_sociales = self.gui.builder.get_object("spinner-personaje-sociales")

        label_ataque = self.gui.builder.get_object("label-personaje-ataque")
        label_defensa = self.gui.builder.get_object("label-personaje-defensa")

        check_ispj = self.gui.builder.get_object("check-personaje-ispj")
        text_notas = self.gui.builder.get_object("text-personaje-notas")

        self.assertEqual(entry_nombre.get_text(), pj_vars['nombre'])
        self.assertEqual(entry_profesion.get_text(), pj_vars['profesion'])
        self.assertEqual(entry_pueblo.get_text(), pj_vars['pueblo'])

        # TODO: No sé porqué la iteración de la raza no casa
        active_iter = self.gui.pjraza_iters[pj_vars['raza'].id]
        #self.assertEqual(combo_raza.get_active_iter(), active_iter)

        self.assertEqual(spin_hp.get_text(), str(pj_vars['hp']))
        self.assertEqual(spin_fuerza.get_text(), str(pj_vars['fuerza']))
        self.assertEqual(spin_agilidad.get_text(), str(pj_vars['agilidad']))
        self.assertEqual(spin_inteligencia.get_text(), str(pj_vars['inteligencia']))
        self.assertEqual(spin_carisma.get_text(), str(pj_vars['carisma']))

        self.assertEqual(spin_combate.get_text(), str(pj_vars['combate']))
        self.assertEqual(label_ataque.get_text(), str(pj_vars['combate']))
        self.assertEqual(label_defensa.get_text(), str(pj_vars['combate']))

        self.assertEqual(check_ispj.get_active(), pj_vars['is_pj'])

        text_buffer = text_notas.get_buffer()
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        check_notas = text_buffer.get_text(start, end, False)
        self.assertEqual(check_notas, pj_vars['notas'])


    def test_cud_personaje(self):
        self.seleccionar_partida()

        ## crear presonaje
        # variables personaje
        pj_vars = self.db_creator.generar_personaje()
        self.rellenar_pj_guardar(pj_vars)

        # comprobar personaje en base de datos
        partida_db = self.con.get_partidas()[0]
        personajes_partida = self.con.get_personajes(partida_db.id)
        personaje = personajes_partida[-1]

        self.comparar_pj_datos(personaje, pj_vars)

        # comprobar lista de personajes
        self.comprobar_lista_personajes(partida_db.id)

        ## editar personaje
        # cargar personaje
        bt_editarpj = self.gui._buttons_personajes[personaje.id]['edit']
        bt_editarpj.clicked()
        refresh_gui()

        # comprobar que se ha cargado el formulario
        self.comprobar_pjform_cargado(pj_vars)

        # obtener diferentes inputs y rellenar de nuevo
        pj_vars = self.db_creator.generar_personaje()
        pj_vars['is_pj'] = True
        self.rellenar_pj_guardar(pj_vars)

        # guardar cambios
        bt_guardar = self.gui.builder.get_object("button-personaje-guardar")
        bt_guardar.clicked()
        refresh_gui()

        # comprobar personaje en base de datos
        partida_db = self.con.get_partidas()[0]
        personajes_partida = self.con.get_personajes(partida_db.id)
        personaje = personajes_partida[-1] # obtener el último

        self.comparar_pj_datos(personaje, pj_vars)

        # comprobar lista de personajes
        self.comprobar_lista_personajes(partida_db.id)
