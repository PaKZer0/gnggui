import unittest

from .controller import Controller

class ControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.con = Controller(test=True)

    def tearDown(self):
        self.con.close_db()
        self.con.drop_db()
    
    def crear_partida(self):
        self.con.crear_partida('El bosque', 'En un bosque oscuro...')
    
    def crear_equipo(self):
        self.con.crear_equipo(
            'Hacha', 
            'Hacha guerrera muy antigua', 
            1,
            1, # ataque
        )
    
    def crear_personaje(self):
        datos = {
            'nombre': 'Salvajius',
            'profesion': 'Pescadero',
            'raza': 1, # Humano
            'pueblo': 'Londaer',
            'fuerza': 4,
            'agilidad': 4,
            'inteligencia': 4,
            'carisma': 4,
            'combate': 4,
            'conocimientos': 4,
            'latrocinio': 4,
            'magia': 4,
            'sociales': 4,
            'partida': 1,
        }
        
        self.con.crear_personaje(datos)
    
    def test_partida(self):
        # gets
        partidas = self.con.get_partidas()
        self.assertEqual(len(partidas), 0)
        
        # create and gets
        self.crear_partida()
        partidas = self.con.get_partidas()
        self.assertEqual(len(partidas), 1)
        
        # get
        partida = self.con.get_partida(1)
        self.assertEqual(partidas[0], partida)
        
        # edit
        self.con.editar_partida(1, 'La gruta', 'Dentro de una gruta...')
        partida = self.con.get_partida(1)
        self.assertEqual(partida.nombre, 'La gruta')
        
        # delete
        self.con.borrar_partida(partida.id)
        partidas = self.con.get_partidas()
        self.assertEqual(len(partidas), 0)
    
    def test_equipo(self):
        # gets
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 0)
        
        # create and gets
        self.crear_equipo()
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 1)
        
        # get
        equipo = self.con.get_equipo(1)
        self.assertEqual(equipos[0], equipo)
        
        # edit
        self.con.editar_equipo(1, 'Toalla de playa', 'Raspa a jierro')
        equipo = self.con.get_equipo(1)
        self.assertEqual(equipo.nombre, 'Toalla de playa')
        
        # delete
        self.con.borrar_equipo(equipo.id)
        equipos = self.con.get_equipos()
        self.assertEqual(len(equipos), 0)
    
    def test_personaje(self):
        # gets
        personajes = self.con.get_personajes()
        self.assertEqual(len(personajes), 0)
        
        # create and gets
        self.crear_partida()
        self.crear_equipo()
        self.crear_personaje()
        personajes = self.con.get_personajes()
        self.assertEqual(len(personajes), 1)


if __name__ == '__main__':
    unittest.main()
