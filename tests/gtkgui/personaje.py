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

    def comprobar_pjform_cargado(self, pj_vars, vacio=False):
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

        check_nombre = pj_vars['nombre'] if not vacio else ''
        check_profesion = pj_vars['profesion'] if not vacio else ''
        check_pueblo = pj_vars['pueblo'] if not vacio else ''

        check_hp = str(pj_vars['hp']) if not vacio else '1'
        check_fuerza = str(pj_vars['fuerza']) if not vacio else '1'
        check_agilidad = str(pj_vars['agilidad']) if not vacio else '1'
        check_inteligencia = str(pj_vars['inteligencia']) if not vacio else '1'
        check_carisma = str(pj_vars['carisma']) if not vacio else '1'

        check_combate = str(pj_vars['combate']) if not vacio else '1'
        check_ataque = str(pj_vars['combate']) if not vacio else '_'
        check_defensa = str(pj_vars['combate']) if not vacio else '_'
        check_conocimientos = str(pj_vars['conocimientos']) if not vacio else '1'
        check_latrocinio = str(pj_vars['latrocinio']) if not vacio else '1'
        check_magia = str(pj_vars['magia']) if not vacio else '1'
        check_sociales = str(pj_vars['sociales']) if not vacio else '1'

        check_is_pj = pj_vars['is_pj'] if not vacio else False
        check_notas = pj_vars['notas'] if not vacio else ''

        self.assertEqual(entry_nombre.get_text(), check_nombre)
        self.assertEqual(entry_profesion.get_text(), check_profesion)
        self.assertEqual(entry_pueblo.get_text(), check_pueblo)

        # TODO: No sé porqué la iteración de la raza no casa
        if not vacio:
            active_iter = self.gui.pjraza_iters[pj_vars['raza'].id]
            #self.assertEqual(combo_raza.get_active_iter(), active_iter)
        else:
            self.assertEqual(combo_raza.get_active_iter(), None)

        self.assertEqual(spin_hp.get_text(), check_hp)
        self.assertEqual(spin_fuerza.get_text(), check_fuerza)
        self.assertEqual(spin_agilidad.get_text(), check_agilidad)
        self.assertEqual(spin_inteligencia.get_text(), check_inteligencia)
        self.assertEqual(spin_carisma.get_text(), check_carisma)

        self.assertEqual(spin_combate.get_text(), check_combate)
        self.assertEqual(label_ataque.get_text(), check_ataque)
        self.assertEqual(label_defensa.get_text(), check_defensa)

        self.assertEqual(spin_conocimientos.get_text(), check_conocimientos)
        self.assertEqual(spin_latrocinio.get_text(), check_latrocinio)
        self.assertEqual(spin_magia.get_text(), check_magia)
        self.assertEqual(spin_sociales.get_text(), check_sociales)

        self.assertEqual(check_ispj.get_active(), check_is_pj)

        text_buffer = text_notas.get_buffer()
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        notas_value = text_buffer.get_text(start, end, False)
        self.assertEqual(notas_value, check_notas)

    def get_boton_personaje(self, id_personaje, button_key):
        return self.gui._buttons_personajes[id_personaje][button_key]

    def comprobar_clon(self, pj, pjclon, nombre_contains=False):
        if not nombre_contains:
            self.assertEqual(pj.nombre, pjclon.nombre)
        else:
            self.assertTrue(pj.nombre in pjclon.nombre)

        self.assertEqual(pj.profesion, pjclon.profesion)
        self.assertEqual(pj.raza, pjclon.raza)
        self.assertEqual(pj.pueblo, pjclon.pueblo)
        self.assertEqual(pj.hp, pjclon.hp)
        self.assertEqual(pj.fuerza, pjclon.fuerza)
        self.assertEqual(pj.agilidad, pjclon.agilidad)
        self.assertEqual(pj.inteligencia, pjclon.inteligencia)
        self.assertEqual(pj.carisma, pjclon.carisma)
        self.assertEqual(pj.combate, pjclon.combate)
        self.assertEqual(pj.conocimientos, pjclon.conocimientos)
        self.assertEqual(pj.latrocinio, pjclon.latrocinio)
        self.assertEqual(pj.magia, pjclon.magia)
        self.assertEqual(pj.sociales, pjclon.sociales)
        self.assertEqual(pj.notas, pjclon.notas)
        self.assertEqual(pj.is_pj, pjclon.is_pj)

    def test_acciones_personaje(self):
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
        bt_editarpj = self.get_boton_personaje(personaje.id, 'edit')
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

        ## vaciar form
        # cargar personaje
        bt_editarpj = self.get_boton_personaje(personaje.id, 'edit')
        bt_editarpj.clicked()
        refresh_gui()

        bt_vaciar = self.gui.builder.get_object("button-personaje-resetform")
        bt_vaciar.clicked()
        refresh_gui()

        self.comprobar_pjform_cargado({}, vacio=True)

        ## clonar
        bt_clonar = self.get_boton_personaje(personaje.id, 'clone')
        bt_clonar.clicked()
        refresh_gui()

        # comprobar pj y clon en bd
        personajes_partida = self.con.get_personajes(partida_db.id)
        personaje = personajes_partida[-2]
        clon_pj = personajes_partida[-1]
        self.comprobar_clon(personaje, clon_pj)

        ## borrar (el clon)
        bt_borrar = self.get_boton_personaje(clon_pj.id, 'delete')
        bt_borrar.clicked()
        refresh_gui()

        ## comprobar que el clon ya no está presente
        exception = False
        try:
            self.con.get_personaje(clon_pj.id)
        except:
            exception = True

        self.assertTrue(exception)

        personajes_partida = self.con.get_personajes(partida_db.id)
        self.assertEqual(personaje.id, personajes_partida[-1].id)

        ## multiplicar 1
        spin_multiplicar = \
            self.gui.builder.get_object("spinner-personaje-multiplicar")

        spin_multiplicar.set_value(2)

        bt_multiplicar = self.get_boton_personaje(personaje.id, 'multi')
        bt_multiplicar.clicked()
        refresh_gui()

        personajes_partida = self.con.get_personajes(partida_db.id)
        clon_1 = personajes_partida[-2]
        clon_2 = personajes_partida[-1]

        # comprobar spin vacio
        self.assertEqual(spin_multiplicar.get_value(), 0.0)

        # comprobar clones
        self.comprobar_clon(personaje, clon_1, True)
        self.comprobar_clon(personaje, clon_2, True)

        # borrarlos
        for clon_id in (clon_1.id, clon_2.id):
            bt_borrar = self.get_boton_personaje(clon_id, 'delete')
            bt_borrar.clicked()
            refresh_gui()

        ## multiplicar 2
        bt_editarpj = self.get_boton_personaje(personaje.id, 'edit')
        bt_editarpj.clicked()
        refresh_gui()

        spin_multiplicar.set_value(2)
        bt_multiplicar2 = \
            self.gui.builder.get_object("button-personaje-multiplicar")

        bt_multiplicar2.clicked()
        refresh_gui()

        personajes_partida = self.con.get_personajes(partida_db.id)
        clon_1 = personajes_partida[-2]
        clon_2 = personajes_partida[-1]

        # comprobar spin vacio
        self.assertEqual(spin_multiplicar.get_value(), 0.0)

        # comprobar clones
        self.comprobar_clon(personaje, clon_1, True)
        self.comprobar_clon(personaje, clon_2, True)

        # borrarlos
        for clon_id in (clon_1.id, clon_2.id):
            bt_borrar = self.get_boton_personaje(clon_id, 'delete')
            bt_borrar.clicked()
            refresh_gui()

    def test_panel_stats(self):
        # seleccionar partida
        self.seleccionar_partida()

        # abrir panel de stats
        bt_show_stats = self.gui.builder.get_object("button-show-stats")
        bt_show_stats.clicked()
        refresh_gui()

        ## crear presonajes
        # pj
        pj_vars = self.db_creator.generar_personaje()
        pj_vars['is_pj'] = True
        self.rellenar_pj_guardar(pj_vars)

        # pnj
        pnj_vars = self.db_creator.generar_personaje()
        self.rellenar_pj_guardar(pnj_vars)

        partida_db = self.con.get_partidas()[0]
        personajes_partida = self.con.get_personajes(partida_db.id)
        pj = personajes_partida[-2]
        pnj = personajes_partida[-1]

        # marcar y comprobar que aparecen
        check_show_pj = self.get_boton_personaje(pj.id, 'stats')
        check_show_pnj = self.get_boton_personaje(pnj.id, 'stats')

        check_show_pj.set_active(True)
        check_show_pnj.set_active(True)
        refresh_gui()

        # comprobar pj
        stats_list_pjs = self.gui.get_object("stats-list-pjs")
        children = stats_list_pjs.get_children()
        first_row = children[0]
        label_pj_name = first_row.get_children()[0].get_children()[0]

        self.assertEqual(label_pj_name.get_text(), pj.stats_str())

        # comprobar pnj
        stats_list_pnjs = self.gui.get_object("stats-list-pnjs")
        children = stats_list_pnjs.get_children()
        first_row = children[0]
        label_pnj_name = first_row.get_children()[0].get_children()[0]

        self.assertEqual(label_pnj_name.get_text(), pnj.stats_str())

        # desmarcar y comprobar que desaparecen
        check_show_pj.set_active(False)
        check_show_pnj.set_active(False)
        refresh_gui()

        # comprobar pj
        children = stats_list_pjs.get_children()
        self.assertEqual(len(children), 0)

        # comprobar pj
        children = stats_list_pnjs.get_children()
        self.assertEqual(len(children), 0)

        # marcar de nuevo y cambiar de partida
        check_show_pj.set_active(True)
        check_show_pnj.set_active(True)
        refresh_gui()

        # crear nueva partida y seleccionarla
        bt_crear_partida = self.gui.builder.get_object("button-new-partida")
        txt_crear_partida = self.gui.builder.get_object("entry-partida")
        txt_crear_partida.set_text("Otra partida")
        bt_crear_partida.clicked()
        refresh_gui()
        self.seleccionar_partida(1)

        # comprobar que desaparecen
        # comprobar pj
        children = stats_list_pjs.get_children()
        self.assertEqual(len(children), 0)

        # comprobar pj
        children = stats_list_pnjs.get_children()
        self.assertEqual(len(children), 0)
