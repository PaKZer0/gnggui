from . import *
from pymouse import PyMouse

class CrudEquipoTest(BaseConDatosGtkGui):
    def test_crear_borrar_equipo_simple(self):
        entry_nombre = self.gui.get_object("entry-equipo-nombre")
        text_descripcion = self.gui.get_object("equipo-text-descripcion")

        equipo_nombre = "Bolsa de dinero"
        equipo_descripcion = "Te la dan gratis pero esta vacía"

        ## crear
        # meter valores
        entry_nombre.set_text(equipo_nombre)
        info_buffer = Gtk.TextBuffer()
        info_buffer.set_text(equipo_descripcion)
        text_descripcion.set_buffer(info_buffer)

        # click en guardar
        bt_guardar = self.gui.get_object("button-equipo-guardar")
        bt_guardar.clicked()
        refresh_gui()

        # comprobar que se han vaciado los inputs
        self.assertEqual(entry_nombre.get_text(), '')

        text_buffer = text_descripcion.get_buffer()
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        check_descripcion = text_buffer.get_text(start, end, False)
        self.assertEqual(check_descripcion, '')

        # comprobar que el equipo se ha creado en bd
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 1)

        equipo = equipos[0]
        self.assertEqual(equipo.nombre, equipo_nombre)
        self.assertEqual(equipo.descripcion, equipo_descripcion)

        ## borrar
        bt_borrar = self.gui._buttons_equipos[equipo.id]['delete']
        bt_borrar.clicked()
        refresh_gui()

        # comprobar que el equipo ya no esta en base de datos
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 0)

        # comprobar que no esta en el listado (no hay botones almacenados)
        self.assertEqual(len(self.gui._buttons_equipos), 0)
