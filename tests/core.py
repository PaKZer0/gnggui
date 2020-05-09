import unittest

from core.core import Core

showlog = False

class TestCore(unittest.TestCase):
    def setUp(self):
        self.core = Core()
        self.pjvalue = 5
        self.pjmod = 2
        self.vsvalue = 4
        self.vsmod = 1
        self.dificultad = 10
        self.delim = '\n============================='

    def log(self, msg):
        if showlog:
            print(msg)

    def separation(self):
        self.log(self.delim)


    def test_sin_oposicion(self):
        text = """
        Tirada sin oposición {}
        habilidad: {}
        mod: {}
        dificultad: {}
        dado: {}
        resultado: {}
        """
        resultado = self.core.sin_oposicion(self.pjvalue, self.dificultad)
        self.separation()
        self.log(text.format(1, self.pjvalue, 0, self.dificultad, self.core.ultimo_dado, resultado))

        resultado = self.core.sin_oposicion(self.pjvalue, self.dificultad, self.pjmod)
        self.separation()
        self.log(text.format(2, self.pjvalue, self.pjmod, self.dificultad, self.core.ultimo_dado, resultado))

    def test_con_oposicion(self):
        text = """
        Tirada con oposición {}
        pjvalue: {}
        pjmod: {}
        dado1: {}
        vsvalue: {}
        vsmod: {}
        dado2: {}
        resultado: {}
        """
        resultado = self.core.con_oposicion(self.pjvalue, self.vsvalue)
        self.separation()
        self.log(text.format(1, self.pjvalue, 0, self.core.dado1, self.vsvalue, 0, self.core.dado2, resultado))

        resultado = self.core.con_oposicion(self.pjvalue, self.vsvalue, self.pjmod, self.vsmod)
        self.separation()
        self.log(text.format(2, self.pjvalue, self.pjmod, self.core.dado1, self.vsvalue, self.vsmod, self.core.dado2, resultado))

    def test_combate(self):
        text_ini = """
        Iniciativa {}
        pjvalue: {}
        pjmod: {}
        dado1: {}
        vsvalue: {}
        vsmod: {}
        dado2: {}
        resultado: {}
        """

        text_combate = """
        Combate {}
        pjvalue: {}
        pjmod: {}
        dado1: {}
        vsvalue: {}
        vsmod: {}
        dado2: {}
        resultado: {}
        """

        resultado = self.core.iniciativa(self.pjvalue, self.vsvalue)
        self.separation()
        self.log(text_ini.format(1, self.pjvalue, 0, self.core.dado1, self.vsvalue, 0, self.core.dado2, resultado))

        resultado = self.core.combate(self.pjvalue, self.vsvalue)
        self.log(text_combate.format(1, self.pjvalue, 0, self.core.dado1, self.vsvalue, 0, self.core.dado2, resultado))

        resultado = self.core.iniciativa(self.pjvalue, self.vsvalue, self.pjmod, self.vsmod)
        self.separation()
        self.log(text_ini.format(2, self.pjvalue, self.pjmod, self.core.dado1, self.vsvalue, self.vsmod, self.core.dado2, resultado))

        resultado = self.core.combate(self.pjvalue, self.vsvalue, self.pjmod, self.vsmod)
        self.log(text_combate.format(2, self.pjvalue, self.pjmod, self.core.dado1, self.vsvalue, self.vsmod, self.core.dado2, resultado))

    def test_combate_m(self):
        text_ini = """
        Iniciativa Mágica {}
        pjvalue: {}
        pjmod: {}
        dado1: {}
        vsvalue: {}
        vsmod: {}
        dado2: {}
        resultado: {}
        """

        text_combate = """
        Combate Mágico {}
        pjvalue: {}
        pjmod: {}
        dado1: {}
        vsvalue: {}
        vsmod: {}
        dado2: {}
        resultado: {}
        """

        resultado = self.core.iniciativa_m(self.pjvalue, self.pjvalue, self.vsvalue, self.vsvalue)
        self.separation()
        self.log(text_ini.format(1, self.pjvalue, 0, self.core.dado1, self.vsvalue, 0, self.core.dado2, resultado))

        resultado = self.core.combatem_m(self.pjvalue, self.vsvalue)
        self.log(text_combate.format(1, self.pjvalue, 0, self.core.dado1, self.vsvalue, 0, self.core.dado2, resultado))

        resultado = self.core.iniciativa_m(self.pjvalue, self.pjvalue, self.vsvalue, self.vsvalue, self.pjmod, self.vsmod)
        self.separation()
        self.log(text_ini.format(2, self.pjvalue, self.pjmod, self.core.dado1, self.vsvalue, self.vsmod, self.core.dado2, resultado))

        resultado = self.core.combatem_m(self.pjvalue, self.vsvalue, self.pjmod, self.vsmod)
        self.log(text_combate.format(2, self.pjvalue, self.pjmod, self.core.dado1, self.vsvalue, self.vsmod, self.core.dado2, resultado))

if __name__ == '__main__':
    unittest.main()
