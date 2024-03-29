import math
import random
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

def divide_in_factors(total, num_sections):
    # https://stackoverflow.com/questions/7788135/split-number-into-sum-components#answer-7788204
    pair_scramble = False

    if total % 2 == 0:
        total = total - 1
        pair_scramble = True

    # paso 1 & 2
    div = int( math.floor(total / num_sections) )
    sections = [div] * num_sections

    # paso 3
    for i in range(0, num_sections):
        if sum(sections) < total:
            sections[i] = sections[i] + 1
        else:
            break

    # paso 4
    for i in range(0, num_sections):
        currentValue = sections[i]
        range_val = currentValue - div
        rand_val = 0

        try:
            rand_val = random.randint( -range_val , range_val )
        except ValueError:
            pass

        if num_sections % 2 == 1 and i == (num_sections - 1):
            # si es impar y es el último
            # operar y salir
            sections[i] = sections[i] + rand_val

            for j in range(0, num_sections):
                if sum(sections) > total:
                    sections[j] = sections[j] - rand_val
                else:
                    break

            break

        if i % 2 == 0:
            # procesar si es índice par
            sections[i] = sections[i] + rand_val
            sections[i+1] = sections[i+1] - rand_val

    # further scramble
    if pair_scramble:
        total = total + 1
        i = random.randint(0, num_sections-1)
        sections[i] = sections[i] + 1

    return sections


class DatabaseCreator:
    __instance = None

    def __init__(self, con, num_players=1):
        # añadir conexión con la que interaccionaremos con la base de datos
        self.con = con
        self.fake = Faker()

        # crear pjs
        personajes = []

        for i in range(0, num_players):
            personajes.append( self.generar_personaje() )

        default_values = {
            'partida': self.generar_partida(),
            'personajes': personajes
        }

        self.default_values = default_values

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = cls(*args, **kwargs)

        return cls.__instance

    ## partida ##
    def generar_partida(self):
        return {
            'nombre': self.fake.company(),
            'descripcion': self.fake.paragraph(),
        }

    def crear_partida(self, nombre=None, descripcion=None):
        if not nombre:
            nombre = self.default_values['partida']['nombre']
            descripcion = self.default_values['partida']['descripcion']

        return self.con.crear_partida(
            nombre=nombre,
            descripcion=descripcion,
        )

    ## personaje ##
    def generar_personaje(self):
        atributos = divide_in_factors(16, 4)
        habilidades = divide_in_factors(20, 5)

        return {
            'nombre': self.fake.first_name(),
            'profesion': self.fake.job(),
            'raza': random.choice(self.con.get_razas()),
            'pueblo': self.fake.city(),
            'hp': atributos[0] * 3,
            'fuerza': atributos[0],
            'agilidad': atributos[1],
            'inteligencia': atributos[2],
            'carisma': atributos[3],
            'combate': habilidades[0],
            'conocimientos': habilidades[1],
            'latrocinio': habilidades[2],
            'magia': habilidades[3],
            'sociales': habilidades[4],
            'notas': self.fake.paragraph(),
            'is_pj': False,
        }

    def crear_personajes(self, id_partida=None):
        for pj_values in self.default_values['personajes']:
            datos = pj_values
            if id_partida:
                datos['partida'] = id_partida

            self.con.crear_personaje(datos=datos)

    def fill_full_db(self):
        partida = self.crear_partida()
        personajes = self.crear_personajes(id_partida=partida.id)


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


class BaseConDatosGtkGui(BaseTestGtkGui):
    def setUp(self):
        con = Controller(True)
        self.db_creator = DatabaseCreator.get_instance(con=con)
        self.db_creator.fill_full_db()
        db_instance = con.get_db()

        super().setUp(db_instance=db_instance)

    def comprobar_combos_personaje(self, id_partida=None):
        if not id_partida:
            id_partida = self.con.get_partidas()[0].id


        combos_pj = []
        combos_pj.append(self.gui.get_object("combo-pj-tirada"))
        combos_pj.append(self.gui.get_object("combo-pnj-tirada"))
        combos_pj.append(self.gui.get_object("combo-pj-combate"))
        combos_pj.append(self.gui.get_object("combo-pnj-combate"))

        personajes_partida = self.con.get_personajes(id_partida)

        for combo_pj in combos_pj:
            i = 0

            for pj_model in combo_pj.get_model():
                pjtest = personajes_partida[i]
                self.assertEqual(pj_model[0], pjtest.id)
                self.assertEqual(pj_model[1], pjtest.combo_str())

                i = i + 1

    def comprobar_lista_personajes(self, id_partida=None):
        if not id_partida:
            id_partida = self.con.get_partidas()[0].id

        list_personaje = self.gui.get_object("list-personajes")
        personajes_partida = self.con.get_personajes(id_partida)

        children = list_personaje.get_children()
        i = 0

        for child in children:
            personaje = personajes_partida[i]
            box = child.get_children()[0]
            box_children = box.get_children()
            txt_pjinlst = box_children[0].get_label()

            self.assertEqual(personaje.combo_str(), txt_pjinlst)

            i = i + 1

    def seleccionar_partida(self, index=0):
        # seleccionar fila
        cselpartida = self.gui.get_object("combo-partida")
        #cselpartida.popup() # quizas no sea necesario ahora
        refresh_gui()
        cselpartida.set_active(index)
        refresh_gui()
        #cselpartida.popdown() # quizás no sea necesario
        refresh_gui()

        # click en cargar
        bt_load_partida = self.gui.builder.get_object("button-load-partida")
        bt_load_partida.clicked()
        refresh_gui()


from .partida import *
from .equipo import *
from .personaje import *
