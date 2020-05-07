import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from unittest import TestCase, main

from gui.gtkgui import run_gui

import time

def refresh_gui(delay=0):
    while Gtk.events_pending():
        Gtk.main_iteration_do(False)

    time.sleep(delay)

class TestGtkGui(TestCase):

    def setUp(self):
        self.gui = run_gui(test=True)

    '''def tearDown(self):
        self._v.exit()'''

    def test_test(self):
        bt_crear_partida = self.gui.builder.get_object("button-new-partida")
        txt_crear_partida = self.gui.builder.get_object("entry-partida")
        txt_crear_partida.set_value('Partida de test')
        refresh_gui()
        #self.gui.exit()
