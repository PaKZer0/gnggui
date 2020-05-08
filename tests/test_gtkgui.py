import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from unittest import TestCase, main
from faker import Faker

from gui.gtkgui import run_gui
from core.models import *

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
                'nombre': fake.catch_phrase(),
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

    def setUp(self):
        init_db(test=True)
        self.gui = run_gui(test=True)
        self.con = self.gui.get_controller()

    def tearDown(self):
        self.con.drop_db()
        self.con.close_db()
        self.gui.exit()


class CrearPartidaTest(BaseTestGtkGui):
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
    def test_borrar_partidad(self):
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
        super().setUp()
        self.db_creator = DatabaseCreator.get_instance(con=self.con)
        self.db_creator.crear_partida()

    def test_cargar_partida(self):
        # seleccionar fila
        cselpartida = self.gui.get_object("combo-partida")
        cselpartida.popup() # quizas no sea necesario ahora
        cselpartida.set_active(0)
        cselpartida.popdown() # quizás no sea necesario

        # click en cargar
        bt_load_partida = self.gui.builder.get_object("button-load-partida")
        bt_load_partida.clicked()
        refresh_gui()

        # comprobar pestañas cargadas
