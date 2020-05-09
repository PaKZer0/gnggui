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


from .partida import *
