import unittest

from core.controller import Controller

class ControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.con = Controller(test=True)

    def tearDown(self):
        self.con.close_db()
        self.con.drop_db()

    def crear_partida(self):
        return self.con.crear_partida('El bosque', 'En un bosque oscuro...')

    def crear_equipo(self):
        return self.con.crear_equipo(
            nombre='Hacha',
            descripcion='Hacha guerrera muy antigua',
            valor=4,
            id_mod=1, # ataque
        )

    def crear_equipo2(self):
        return self.con.crear_equipo(
            nombre='Escudo de cartón',
            descripcion='Si se moja adiós',
            valor=-1,
            id_mod=2, # defensa
        )

    def crear_equipom1(self):
        mod_magia = self.con.get_mod(9)
        return self.con.crear_equipo(
            nombre='Báculo de napalm',
            descripcion='Magia abrasadora',
            valor=4,
            id_mod=mod_magia.id,
        )

    def crear_equipom2(self):
        mod_magia = self.con.get_mod(9)
        return self.con.crear_equipo(
            nombre='Cardo borriquero',
            descripcion='Dicen que da suerte',
            valor=1,
            id_mod=mod_magia.id,
        )

    def crear_personaje(self, nombre=None):
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
            'raza': 6, # Goblin
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
        self.con.editar_equipo(
            id_equipo=1, nombre='Toalla de playa', descripcion='Raspa a jierro')
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
        personajes = self.con.get_personajes(1) # id_partida
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

    def test_personaje_partida(self):
        # create and gets
        partida = self.crear_partida()
        personaje = self.crear_personaje()

        # personaje_en_partida
        pj_en_partida = self.con.personaje_en_partida(personaje.id, partida.id)
        self.assertTrue(pj_en_partida, "El personaje debe existir en la partida")

        partida2 = self.con.crear_partida('La sombra', 'La vuelta de la sombra...')
        pj_en_partida = self.con.personaje_en_partida(personaje.id, partida2.id)
        self.assertFalse(pj_en_partida, "El personaje no debe existir en la partida")

        # get_personajes_disponibles
        pj_disponibles = self.con.get_personajes_disponibles(partida2.id)
        self.assertEqual(pj_disponibles, [personaje])

        pj_disponibles = self.con.get_personajes_disponibles(partida.id)
        self.assertEqual(pj_disponibles, [])

        # asignar_personaje_partida
        self.con.asignar_personaje_partida(personaje.id, partida2.id)
        pj_en_partida = self.con.personaje_en_partida(personaje.id, partida2.id)
        self.assertTrue(pj_en_partida, "El personaje debe existir en la partida")

        # get_partidas_personaje
        partidas_pj = self.con.get_partidas_personaje(personaje.id)
        self.assertTrue(len(partidas_pj) == 2, "El personaje existe en 2 partidas")
        puede = self.con.puede_quitar_pj_partida(personaje.id)
        self.assertTrue(puede)

        # quitar_personaje_partida
        self.con.quitar_personaje_partida(personaje.id, partida2.id)
        pj_en_partida = self.con.personaje_en_partida(personaje.id, partida2.id)
        self.assertFalse(pj_en_partida, "El personaje no debe existir en la partida")
        puede = self.con.puede_quitar_pj_partida(personaje.id)
        self.assertFalse(puede)

        pjs_partida1 = self.con.get_personajes(partida.id)
        self.assertEqual(pjs_partida1, [personaje])

        pj_disponibles = self.con.get_personajes_disponibles(partida2.id)
        self.assertEqual(pj_disponibles, [personaje])
        pj_disponibles = self.con.get_personajes_disponibles(partida.id)
        self.assertEqual(pj_disponibles, [])

        # probamos con 2 jugadores
        adversario = self.crear_adversario()
        pj_disponibles = self.con.get_personajes_disponibles(partida.id)
        self.assertEqual(pj_disponibles, [])
        pj_disponibles = self.con.get_personajes_disponibles(partida2.id)
        self.assertEqual(pj_disponibles, [personaje, adversario])

        self.con.asignar_personaje_partida(adversario.id, partida2.id)
        pj_disponibles = self.con.get_personajes_disponibles(partida2.id)
        self.assertEqual(pj_disponibles, [personaje])

    def test_asignar_robar(self):
        self.crear_partida()
        equipo =self.crear_equipo()
        personaje = self.crear_personaje()

        equipos = self.con.get_equipos_personaje(personaje.id)
        self.assertEqual(len(equipos), 0)

        rel = self.con.asignar_equipo(personaje.id, equipo.id)
        equipos = self.con.get_equipos_personaje(personaje.id)
        self.assertEqual(len(equipos), 1)

        self.con.desasignar_equipo(rel.id)
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

    def test_iniciativa(self):
        self.crear_partida()
        personaje = self.crear_personaje()
        adversario = self.crear_adversario()
        mod_agilidad = self.con.get_mod(4)
        mod_magia = self.con.get_mod(9)

        equipo1 = self.con.crear_equipo(
            'Zapatos de puma',
            'Superágil al instante',
            4,
            mod_agilidad.id,
        )

        equipom1 = self.con.crear_equipo(
            'Báculo de napalm',
            'Magia abrasadora',
            4,
            mod_magia.id,
        )

        self.con.asignar_equipo(personaje.id, equipo1.id)
        self.con.asignar_equipo(personaje.id, equipom1.id)

        equipo2 = self.con.crear_equipo(
            'Zapatos de plomo',
            'Clavado al suelo',
            -4,
            mod_agilidad.id,
        )

        equipom2 = self.con.crear_equipo(
            'Cardo borriquero',
            'Dicen que da suerte',
            0,
            mod_magia.id,
        )

        self.con.asignar_equipo(adversario.id, equipo2.id)
        self.con.asignar_equipo(adversario.id, equipom2.id)

        # iniciativa normal
        ret_tirada = self.con.iniciativa(
            personaje.id,
            adversario.id,
        )

        # debería de empezar el pj
        self.assertTrue(ret_tirada['resultado'])

        # iniciativa magica
        ret_tirada = self.con.iniciativa(
            personaje.id,
            adversario.id,
            True,
            4,
            -4,
        )

        # debería de empezar el pj
        self.assertTrue(ret_tirada['resultado'])

    def test_combate(self):
        self.crear_partida()
        personaje = self.crear_personaje()
        adversario = self.crear_adversario()

        equipo1 = self.crear_equipo()
        equipo2 = self.crear_equipo2()
        equipom1 = self.crear_equipom1()
        equipom2 = self.crear_equipom2()

        self.con.asignar_equipo(personaje.id, equipo1.id)
        self.con.asignar_equipo(personaje.id, equipom1.id)
        self.con.asignar_equipo(adversario.id, equipo2.id)
        self.con.asignar_equipo(adversario.id, equipom2.id)

        # combate normal
        ret_tirada = self.con.combate(
            personaje.id,
            adversario.id,
            magia=False,
            bonus_ata=2, # got higher ground
            bonus_def=-2,
        )

        # debería de golpear el pj
        self.assertTrue( ret_tirada['resultado'] > 0 )

        # combate mágico
        ret_tirada = self.con.combate(
            personaje.id,
            adversario.id,
            magia=True,
            bonus_ata=2, # got higher ground
            bonus_def=-2,
        )

        # debería de golpear el pj
        self.assertTrue( ret_tirada['resultado'] > 0 )


    def test_equipo_m(self):
        self.crear_partida()
        personaje = self.crear_personaje()
        adversario = self.crear_adversario()

        equipo1 = self.crear_equipo()
        equipo2 = self.crear_equipo2()
        equipom1 = self.crear_equipom1()
        equipom2 = self.crear_equipom2()

        self.con.asignar_equipo(personaje.id, equipo1.id)
        self.con.asignar_equipo(personaje.id, equipom1.id)
        self.con.asignar_equipo(adversario.id, equipo2.id)
        self.con.asignar_equipo(adversario.id, equipom2.id)

        mod_magia = self.con.get_mod(9)

        magia_pjvalue  = self.con.bonus_mod_personaje(mod_magia, personaje)
        magia_pnjvalue = self.con.bonus_mod_personaje(mod_magia, adversario)

        self.assertEqual(magia_pjvalue, 4)
        self.assertEqual(magia_pnjvalue, 1)


if __name__ == '__main__':
    unittest.main()
