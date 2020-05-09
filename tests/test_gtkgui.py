import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from unittest import TestCase, main
from faker import Faker

from gui.gtkgui import run_gui
from core.models import init_db
from core.controller import Controller

# http://unpythonic.blogspot.com/2007/03/unit-testing-pygtk.html
def refresh_gui(delay=0):
    while Gtk.events_pending():
        Gtk.main_iteration_do(False)

    time.sleep(delay)


class DatabaseCreator:
    __instance = None

    def __init__(self, con):
        # añadir conexión con la que interaccionaremos con la base de datos
        self.con = con

        fake = Faker()
        default_values = {
            'partida':{
                'nombre': fake.company(),
                'descripcion': fake.paragraph(),
            }
        }

        self.default_values = default_values

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = cls(*args, **kwargs)

        return cls.__instance

    def fill_full_db(self):
        self.run_crear_partida()

    def crear_partida(self):
        return self.con.crear_partida(
            nombre=self.default_values['partida']['nombre'],
            descripcion=self.default_values['partida']['descripcion'],
        )


class BaseTestGtkGui(TestCase):
    def creat_partida(self, bt_crear_partida, txt_crear_partida):
        txt_partida = "Una nueva aventura"
        txt_crear_partida.set_text(txt_partida)
        bt_crear_partida.clicked()
        refresh_gui()

        return txt_partida

    def setUp(self, db_instance=None):
        self.gui = run_gui(test=True, db_instance=db_instance)
        self.con = self.gui.get_controller()

    def tearDown(self):
        self.con.drop_db()
        self.con.close_db()
        self.gui.exit()


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


class CargarPartidaTest(BaseTestGtkGui):
    def setUp(self):
        con = Controller(True)
        self.db_creator = DatabaseCreator.get_instance(con=con)
        self.db_creator.crear_partida()
        db_instance = con.get_db()

        super().setUp(db_instance=db_instance)

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

    def test_cargar_partida(self):
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
        text_buffer = self.gui.get_object("text-partida-descripcion")\
                                .get_buffer()
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        txt_descripcion = text_buffer.get_text(start, end, False)

        db_descripcion = self.con.get_partidas()[0].descripcion

        self.assertEqual(txt_descripcion, db_descripcion)
