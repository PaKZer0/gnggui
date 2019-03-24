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
        
        personaje = self.con.crear_personaje(datos)
        return personaje
    
    def crear_adversario(self):
        datos = {
            'nombre': 'Gork',
            'profesion': 'Artillero',
            'raza': 6, # Humano
            'pueblo': 'Morgul',
            'fuerza': 2,
            'agilidad': 2,
            'inteligencia': 2,
            'carisma': 1,
            'combate': 2,
            'conocimientos': 1,
            'latrocinio': 5,
            'magia': 1,
            'sociales': 1,
            'partida': 1,
        }
        
        adversario = self.con.crear_personaje(datos)
        return adversario
    
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
        
        # get
        personaje = self.con.get_personaje(1)
        self.assertEqual(personajes[0], personaje)
        
        # edit
        datos = {
            'nombre': 'Nunambaril',
        }
        personaje = self.con.editar_personaje(1, datos)
        self.assertEqual(personaje.nombre, 'Nunambaril')
        
        # delete
        self.con.borrar_personaje(personaje.id)
        personajes = self.con.get_personajes()
        self.assertEqual(len(personajes), 0)
    
    def test_asignar_robar(self):
        self.crear_partida()
        self.crear_equipo()
        self.crear_personaje()
        
        personaje = self.con.get_personaje(1)
        equipo = self.con.get_equipo(1)
        
        equipos = self.con.get_equipos_personaje(personaje.id)
        self.assertEqual(len(equipos), 0)
        
        self.con.asignar_equipo(personaje.id, equipo.id)
        equipos = self.con.get_equipos_personaje(personaje.id)
        self.assertEqual(len(equipos), 1)
        
        self.con.robar_equipo(personaje.id, equipo.id)
        equipos = self.con.get_equipos_personaje(personaje.id)
        self.assertEqual(len(equipos), 0)
    
    def test_tirada_sin(self):
        self.crear_partida()
        personaje = self.crear_personaje()
        dificultad = self.con.get_dificultad(1)
        
        # create cuerda
        mod_agilidad = self.con.get_mod(4)
        equipo = self.con.crear_equipo(
            'Cuerda', 
            'Sirve para escalar', 
            4,
            mod_agilidad.id,
        )
        
        self.con.asignar_equipo(personaje.id, equipo.id)
        
        ret_tirada = self.con.tirada_sin_oposicion(
            personaje.id,
            dificultad.id,
            mod_agilidad.id
        )
        
        # debería de lograrlo
        self.assertTrue(ret_tirada['resultado'])
    
    def test_tirada_con(self):
        self.crear_partida()
        personaje = self.crear_personaje()
        adversario = self.crear_adversario()
        
        # create libro
        mod_inteligencia = self.con.get_mod(4)
        equipo = self.con.crear_equipo(
            'Libro', 
            'Te hace mas inteligente',
            4,
            mod_inteligencia.id,
        )
        
        self.con.asignar_equipo(personaje.id, equipo.id)
        
        ret_tirada = self.con.tirada_con_oposicion(
            personaje.id,
            adversario.id,
            mod_inteligencia.id,
            2
        )
        
        # debería de lograrlo
        self.assertTrue(ret_tirada['resultado'])


if __name__ == '__main__':
    unittest.main()
