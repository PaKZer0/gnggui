from . import *

class CrearPartidaTest(BaseTestGtkGui):
    def setUp(self, db_instance=None):
        init_db(test=True, db_instance=db_instance)
        super().setUp(db_instance=db_instance)

    def test_crear_partida(self):
        bt_crear_partida = self.gui.builder.get_object("button-new-partida")
        txt_crear_partida = self.gui.builder.get_object("entry-partida")
        txt_partida = self.creat_partida(bt_crear_partida, txt_crear_partida)

        refresh_gui()

        # comprobar que el entry de nombre de partida se ha vaciado
        txt_entry_partida = txt_crear_partida.get_text()
        self.assertIs(txt_entry_partida, '')

        # comprobar que la partida se ha creado en base de datos
        partidas = self.con.get_partidas()
        self.assertIsNot(partidas, [])

        # comprobar el nombre de la partida
        nombre_partida = partidas[0].nombre
        self.assertEqual(txt_partida, nombre_partida)

        # comprobar que se ha cargado en el combo de partidas
        cselpartida = self.gui.get_object("combo-partida")
        nombre_partida = cselpartida.get_model()[0][1]
        id_partida = cselpartida.get_model()[0][0]
        self.assertEqual(txt_partida, nombre_partida)
        self.assertEqual(id_partida, partidas[0].id)


class BorrarPartidaTest(BaseTestGtkGui):
    def test_borrar_partida(self):
        bt_crear_partida = self.gui.builder.get_object("button-new-partida")
        bt_borrar_partida = self.gui.builder.get_object("button-remove-partida")
        txt_crear_partida = self.gui.builder.get_object("entry-partida")
        txt_partida = self.creat_partida(bt_crear_partida, txt_crear_partida)

        # seleccionar fila
        cselpartida = self.gui.get_object("combo-partida")
        cselpartida.popup() # quizas no sea necesario ahora
        cselpartida.set_active(0)
        cselpartida.popdown() # quizás no sea necesario

        # click en cargar
        bt_borrar_partida.clicked()
        refresh_gui()

        # comprobar que el combo se ha refrescado y esta vacio
        cselpartida = self.gui.get_object("combo-partida")
        partidas_comboentries = [x for x in cselpartida.get_model()]
        self.assertEqual(partidas_comboentries, [])

        # comprobar que la partida no existe en base de datos
        partidas = self.con.get_partidas()
        self.assertEqual(partidas, [])


class CargarPartidaTest(BaseConDatosGtkGui):
    def comprobar_pestanyas(self, should_be_active=True):
        tab1 = self.gui.builder.get_object("tab-partida")
        tab2 = self.gui.builder.get_object("tab-equipo")
        tab3 = self.gui.builder.get_object("tab-personaje")
        tab4 = self.gui.builder.get_object("tab-tiradas")
        tab5 = self.gui.builder.get_object("tab-combate")

        assert_function = 'assertFalse'

        if should_be_active:
            assert_function = 'assertTrue'

        getattr(self, assert_function)(tab1.is_sensitive())
        getattr(self, assert_function)(tab3.is_sensitive())
        getattr(self, assert_function)(tab4.is_sensitive())
        getattr(self, assert_function)(tab5.is_sensitive())

    def test_cargar_editar_partida(self):
        ## cargar
        # comprobar partida presente en combo
        cselpartida = self.gui.get_object("combo-partida")
        partidas_comboentries = [x for x in cselpartida.get_model()]
        self.assertEqual(len(partidas_comboentries), 1)

        # comprobar pestañas desactivadas
        self.comprobar_pestanyas(should_be_active=False)

        # seleccionar fila
        cselpartida.popup() # quizas no sea necesario ahora
        refresh_gui()
        cselpartida.set_active(0)
        refresh_gui()
        cselpartida.popdown() # quizás no sea necesario
        refresh_gui()

        # click en cargar
        bt_load_partida = self.gui.builder.get_object("button-load-partida")
        bt_load_partida.clicked()
        refresh_gui()

        # comprobamos que se ha cargado la partida internamente
        partida_cargada = getattr(self.gui, 'partida', None)
        self.assertNotEqual(partida_cargada, None)

        # comprobar pestañas activas
        self.comprobar_pestanyas()

        # comprobar título de la partida
        partida_db = self.con.get_partidas()[0]
        entry_nombre = self.gui.get_object("entry-partida-name")
        txt_nombre = entry_nombre.get_text()
        db_nombre = partida_db.nombre
        self.assertEqual(txt_nombre, db_nombre)

        # comprobar descripción de la partida
        texta_descripcion = self.gui.get_object("text-partida-descripcion")
        text_buffer = texta_descripcion.get_buffer()
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        txt_descripcion = text_buffer.get_text(start, end, False)

        db_descripcion = partida_db.descripcion

        self.assertEqual(txt_descripcion, db_descripcion)

        ## editar
        # cambiar nombre y descripción
        new_partida = self.db_creator.generar_partida()
        new_nombre = new_partida['nombre']
        new_descripcion = new_partida['descripcion']

        entry_nombre.set_text(new_nombre)
        info_buffer = Gtk.TextBuffer()
        info_buffer.set_text(new_descripcion)
        texta_descripcion.set_buffer(info_buffer)
        refresh_gui()

        # guardamos
        bt_edit_partida = self.gui.builder.get_object("button-edit-partida")
        bt_edit_partida.clicked()
        refresh_gui()

        # comprobar que los valores han cambiado en base de datos
        partida_db = self.con.get_partidas()[0]
        db_nombre = partida_db.nombre
        db_descripcion = partida_db.descripcion

        self.assertEqual(new_nombre, db_nombre)
        self.assertEqual(new_descripcion, db_descripcion)

        # comprobar que se ha cambiado el valor en el combo de partidas
        cselpartida = self.gui.get_object("combo-partida")
        nombre_partida = cselpartida.get_model()[0][1]
        self.assertEqual(new_nombre, nombre_partida)

        # comprobar que se cargan los personajes en los combos
        combos_pj = []
        combos_pj.append(self.gui.get_object("combo-pj-tirada"))
        combos_pj.append(self.gui.get_object("combo-pnj-tirada"))
        combos_pj.append(self.gui.get_object("combo-pj-combate"))
        combos_pj.append(self.gui.get_object("combo-pnj-combate"))

        personajes_partida = self.con.get_personajes(partida_db.id)

        for combo_pj in combos_pj:
            i = 0

            for pj_model in combo_pj.get_model():
                pjtest = personajes_partida[i]
                self.assertEqual(pj_model[0], pjtest.id)
                self.assertEqual(pj_model[1], pjtest.combo_str())

                i = i + 1

        # comprobar que se carga la lista de personajes
