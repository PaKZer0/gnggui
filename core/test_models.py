import unittest

from .core import Core
from .models import *

MODELS = [Dificultad, Partida, Raza, Mod, Equipo, Player, PlayerEquipo]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)
        
        # create primitives
        for raza in RAZAS:
            Raza.create(nombre=raza[1])
		
        for modtype in MOD_TYPE:
            Mod.create(nombre=modtype[1])
        
        for dif in DIFICULTADES:
            Dificultad.create(valor=dif[0], texto=dif[1])
        
        self.partida = Partida.create(nombre="Partida test")
        self.core = Core()

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

        # If we wanted, we could re-bind the models to their original
        # database here. But for tests this is probably not necessary.
    
    def test_player_equipo(self):
        r_elfo = Raza.get(Raza.nombre == 'Elfo')
        r_goblin = Raza.get(Raza.nombre == 'Goblin')

        self.pj1 = Player.create(
            nombre="Eldelpan",
            profesion="Panadero",
            raza =r_elfo,
            pueblo="Sindar",
            hp=(4*5),
            fuerza=4,
            agilidad=4,
            inteligencia=4,
            carisma=4,
            combate=4,
            conocimientos=4,
            latrocinio=4,
            magia=4,
            sociales=4,
            partida=self.partida
        )
        
        self.pnj = Player.create(
            nombre="Ugluk el mierda",
            profesion="Basurero",
            raza =r_goblin,
            pueblo="Montañas",
            hp=(3*5),
            fuerza=4,
            agilidad=4,
            inteligencia=4,
            carisma=4,
            combate=4,
            conocimientos=4,
            latrocinio=4,
            magia=4,
            sociales=4,
            partida=self.partida
        )
        
        m_ataque  = Mod.get(Mod.nombre == "Ataque")
        m_defensa = Mod.get(Mod.nombre == "Defensa")
        m_intelig = Mod.get(Mod.nombre == "Inteligencia")
        m_magia   = Mod.get(Mod.nombre == "Magia")
        
        self.arma1 = Equipo.create(
            nombre="Espada élfica",
            valor=2,
            mod=m_ataque,
        )
        
        self.arma2 = Equipo.create(
            nombre="Pincho orco",
            valor=-1,
            mod=m_ataque,
        )
        
        self.escudo1 = Equipo.create(
            nombre="Escudo élfico",
            valor=3,
            mod=m_defensa,
        )
        
        self.escudo2 = Equipo.create(
            nombre="Tapa de cubo de basura",
            valor=-2,
            mod=m_defensa,
        )
        
        self.item1 = Equipo.create(
            nombre="Libro de hechizos",
            valor=3,
            mod=m_magia,
        )
        
        self.item2 = Equipo.create(
            nombre="Libro de ciencia",
            valor=3,
            mod=m_intelig,
        )
        
        PlayerEquipo.create(
            player=self.pj1,
            equipo=self.arma1,
        )
        
        PlayerEquipo.create(
            player=self.pj1,
            equipo=self.escudo1,
        )
        
        PlayerEquipo.create(
            player=self.pnj,
            equipo=self.arma2,
        )
        
        PlayerEquipo.create(
            player=self.pnj,
            equipo=self.escudo2,
        )
        
        PlayerEquipo.create(
            player=self.pj1,
            equipo=self.item1,
        )
        
        PlayerEquipo.create(
            player=self.pj1,
            equipo=self.item2,
        )


if __name__ == '__main__':
    unittest.main()
