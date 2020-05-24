from . import *

class CrudEquipoTest(BaseConDatosGtkGui):
    def rellenar_formulario(self, entry_nombre, text_descripcion, bt_guardar,
                            sp_valor, combo_mod, sp_unidades, combo_equipo_asociado,
                            equipo_nombre, equipo_descripcion, equipo_valor,
                            equipo_i_mod, equipo_unidades,
                            equipo_asociado=None):
        # meter valores
        entry_nombre.set_text(equipo_nombre)
        info_buffer = Gtk.TextBuffer()
        info_buffer.set_text(equipo_descripcion)
        text_descripcion.set_buffer(info_buffer)
        sp_valor.set_value(equipo_valor)
        sp_unidades.set_value(equipo_unidades)

        if equipo_i_mod:
            combo_mod.set_active(equipo_i_mod)
        else:
            combo_mod.set_active(-1)

        if equipo_asociado:
            combo_equipo_asociado.set_active(equipo_asociado.id)
        else:
            combo_equipo_asociado.set_active(-1)

        refresh_gui()

        # click en guardar
        bt_guardar.clicked()
        refresh_gui()

    def comprobar_inputs_vacios(self, entry_nombre, text_descripcion, sp_valor,
                                combo_mod, sp_unidades, combo_equipo_asociado):
        self.assertEqual(entry_nombre.get_text(), '')

        text_buffer = text_descripcion.get_buffer()
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        check_descripcion = text_buffer.get_text(start, end, False)
        self.assertEqual(check_descripcion, '')

        self.assertEqual(sp_valor.get_value_as_int(), 0)
        self.assertEqual(combo_mod.get_active_iter(), None)
        self.assertEqual(sp_unidades.get_value_as_int(), 0)
        self.assertEqual(combo_equipo_asociado.get_active_iter(), None)

    def comprobar_equipo_bd(self, equipo, equipo_nombre, equipo_descripcion,
                            equipo_valor, equipo_mod, equipo_unidades,
                            equipo_equipoasociado=None):
        self.assertEqual(equipo.nombre, equipo_nombre)
        self.assertEqual(equipo.descripcion, equipo_descripcion)
        self.assertEqual(equipo.valor, equipo_valor)
        self.assertEqual(equipo.mod, equipo_mod)
        self.assertEqual(equipo.unidades, equipo_unidades)
        self.assertEqual(equipo.equipo_asociado, equipo_equipoasociado)

    def test_cud_equipo(self):
        entry_nombre = self.gui.get_object("entry-equipo-nombre")
        text_descripcion = self.gui.get_object("equipo-text-descripcion")
        bt_guardar = self.gui.get_object("button-equipo-guardar")
        sp_valor = self.gui.get_object("spin-equipo-valor")
        combo_mod = self.gui.get_object("combo-equipo-mod")
        sp_unidades = self.gui.get_object("spin-equipo-unidades")
        combo_equipo_asociado = self.gui.get_object("combo-equipo-asociado")

        equipo_nombre = "Bolsa de piedras"
        equipo_descripcion = "Un kit estupendo para jugar a los chinos"
        equipo_i_mod = 10 # Sociales
        equipo_mod = self.con.get_mods()[ equipo_i_mod - 1 ] # opcion vacia
        equipo_valor = 0
        equipo_unidades = 10

        ## crear
        # meter valores
        self.rellenar_formulario(entry_nombre, text_descripcion, bt_guardar,
                                sp_valor, combo_mod, sp_unidades,
                                combo_equipo_asociado, equipo_nombre,
                                equipo_descripcion, equipo_valor, equipo_i_mod,
                                equipo_unidades)

        # comprobar que se han vaciado los inputs
        self.comprobar_inputs_vacios(entry_nombre, text_descripcion, sp_valor,
                                        combo_mod, sp_unidades,
                                        combo_equipo_asociado)

        # comprobar que el equipo se ha creado en bd
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 1)

        equipo = equipos[0]
        self.comprobar_equipo_bd(equipo, equipo_nombre, equipo_descripcion,
                            equipo_valor, equipo_mod, equipo_unidades)

        ## añadir otro equipo
        equipo2_nombre = "Tirachinas"
        equipo2_descripcion = "Convierte un ajedrez en munición"
        equipo2_i_mod = None
        equipo2_valor = 1
        equipo2_unidades = 0
        equipo2_equipo_asociado = equipo
        self.rellenar_formulario(entry_nombre, text_descripcion, bt_guardar,
                                sp_valor, combo_mod, sp_unidades,
                                combo_equipo_asociado, equipo2_nombre,
                                equipo2_descripcion, equipo2_valor,
                                equipo2_i_mod, equipo2_unidades,
                                equipo2_equipo_asociado)

        # comprobar que el equipo se ha creado en bd
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 2)
        equipo2 = equipos[1]

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
                                        combo_mod, sp_unidades,
                                        combo_equipo_asociado)

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
        equipo_unidades = 0
        equipo_equipo_asociado = None

        self.rellenar_formulario(entry_nombre, text_descripcion, bt_guardar,
                                sp_valor, combo_mod, sp_unidades,
                                combo_equipo_asociado, equipo_nombre,
                                equipo_descripcion, equipo_valor, equipo_i_mod,
                                equipo_unidades, equipo_equipo_asociado)

        # comprobar que se han vaciado los inputs
        self.comprobar_inputs_vacios(entry_nombre, text_descripcion, sp_valor,
                                        combo_mod, sp_unidades,
                                        combo_equipo_asociado)

        # comprobar que el equipo se ha actualizado en bd
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 2)

        equipo = equipos[0]
        self.comprobar_equipo_bd(equipo, equipo_nombre, equipo_descripcion,
                            equipo_valor, equipo_mod, equipo_unidades,
                            equipo_equipo_asociado)

        ## delete
        bt_borrar = self.gui._buttons_equipos[equipo.id]['delete']
        bt_borrar.clicked()
        refresh_gui()

        bt_borrar = self.gui._buttons_equipos[equipo2.id]['delete']
        bt_borrar.clicked()
        refresh_gui()

        # comprobar que el equipo ya no esta en base de datos
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 0)

        # comprobar que no esta en el listado (no hay botones almacenados)
        self.assertEqual(len(self.gui._buttons_equipos), 0)
