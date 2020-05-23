from . import *

class CrudEquipoTest(BaseConDatosGtkGui):
    def rellenar_formulario(self, entry_nombre, text_descripcion, bt_guardar,
                            sp_valor, combo_mod, equipo_nombre,
                            equipo_descripcion, equipo_valor, equipo_i_mod):
        # meter valores
        entry_nombre.set_text(equipo_nombre)
        info_buffer = Gtk.TextBuffer()
        info_buffer.set_text(equipo_descripcion)
        text_descripcion.set_buffer(info_buffer)
        sp_valor.set_value(equipo_valor)
        combo_mod.set_active(equipo_i_mod)
        refresh_gui()

        # click en guardar
        bt_guardar.clicked()
        refresh_gui()

    def comprobar_inputs_vacios(self, entry_nombre, text_descripcion, sp_valor,
                                combo_mod):
        self.assertEqual(entry_nombre.get_text(), '')

        text_buffer = text_descripcion.get_buffer()
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        check_descripcion = text_buffer.get_text(start, end, False)
        self.assertEqual(check_descripcion, '')

        self.assertEqual(sp_valor.get_value_as_int(), 0)
        self.assertEqual(combo_mod.get_active_iter(), None)

    def comprobar_equipo_bd(self, equipo, equipo_nombre, equipo_descripcion,
                            equipo_valor, equipo_mod):
        self.assertEqual(equipo.nombre, equipo_nombre)
        self.assertEqual(equipo.descripcion, equipo_descripcion)
        self.assertEqual(equipo.valor, equipo_valor)
        self.assertEqual(equipo.mod, equipo_mod)

    def test_cud_equipo(self):
        entry_nombre = self.gui.get_object("entry-equipo-nombre")
        text_descripcion = self.gui.get_object("equipo-text-descripcion")
        bt_guardar = self.gui.get_object("button-equipo-guardar")
        sp_valor = self.gui.get_object("spin-equipo-valor")
        combo_mod = self.gui.get_object("combo-equipo-mod")

        equipo_nombre = "Bolsa de dinero"
        equipo_descripcion = "Te la dan gratis pero esta vacía"
        equipo_i_mod = 10 # Sociales
        equipo_mod = self.con.get_mods()[ equipo_i_mod - 1 ] # opcion vacia
        equipo_valor = 1

        ## crear
        # meter valores
        self.rellenar_formulario(entry_nombre, text_descripcion, bt_guardar,
                                sp_valor, combo_mod, equipo_nombre,
                                equipo_descripcion, equipo_valor, equipo_i_mod)

        # comprobar que se han vaciado los inputs
        self.comprobar_inputs_vacios(entry_nombre, text_descripcion, sp_valor,
                                        combo_mod)

        # comprobar que el equipo se ha creado en bd
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 1)

        equipo = equipos[0]
        self.comprobar_equipo_bd(equipo, equipo_nombre, equipo_descripcion,
                            equipo_valor, equipo_mod)

        ## update (y nuevo)
        bt_editar = self.gui._buttons_equipos[equipo.id]['edit']
        bt_editar.clicked()
        refresh_gui()

        # probar nuevo
        bt_nuevo = self.gui.get_object("button-equipo-nuevo")
        bt_nuevo.clicked()
        refresh_gui()

        # comprobar que se han vaciado los inputs
        self.comprobar_inputs_vacios(entry_nombre, text_descripcion, sp_valor,
                                        combo_mod)

        # volver a editar
        bt_editar = self.gui._buttons_equipos[equipo.id]['edit']
        bt_editar.clicked()
        refresh_gui()

        # comprobar que se han cargado los valores en los inputs
        self.assertEqual(entry_nombre.get_text(), equipo_nombre)

        text_buffer = text_descripcion.get_buffer()
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        check_descripcion = text_buffer.get_text(start, end, False)
        self.assertEqual(check_descripcion, equipo_descripcion)

        equipo_nombre = "Trozo de guita"
        equipo_descripcion = "Llevarlo en el inventario demuestra astucia"
        equipo_i_mod = 6 # Carisma
        equipo_mod = self.con.get_mods()[ equipo_i_mod - 1 ] # opcion vacia
        equipo_valor = 3

        self.rellenar_formulario(entry_nombre, text_descripcion, bt_guardar,
                                sp_valor, combo_mod, equipo_nombre,
                                equipo_descripcion, equipo_valor, equipo_i_mod)

        # comprobar que se han vaciado los inputs
        self.comprobar_inputs_vacios(entry_nombre, text_descripcion, sp_valor,
                                        combo_mod)

        # comprobar que el equipo se ha actualizado en bd
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 1)

        equipo = equipos[0]
        self.comprobar_equipo_bd(equipo, equipo_nombre, equipo_descripcion,
                            equipo_valor, equipo_mod)

        ## delete
        bt_borrar = self.gui._buttons_equipos[equipo.id]['delete']
        bt_borrar.clicked()
        refresh_gui()

        # comprobar que el equipo ya no esta en base de datos
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 0)

        # comprobar que no esta en el listado (no hay botones almacenados)
        self.assertEqual(len(self.gui._buttons_equipos), 0)
