from .core import Core
from .models import *

class Controller():
    def __init__(self, test=False):
        init_db(test)
        self.core = Core()

    def close_db(self):
        close_db()

    def drop_db(self):
        drop_db()

    ### PARTIDAS ###
    def get_partidas(self):
        partidas = Partida.select()
        ret = [partida for partida in partidas]

        return ret

    def get_partida(self, id_partida):
        partida = Partida.get(Partida.id == id_partida)

        return partida

    def crear_partida(self, nombre, descripcion=None):
        partida = Partida.create(
            nombre = nombre,
            descripcion = descripcion,
        )

        partida.save()

        return partida

    def editar_partida(self, id_partida, nombre, descripcion):
        partida = Partida.get(Partida.id == id_partida)
        partida.nombre = nombre
        partida.descripcion = descripcion

        partida.save()

        return partida

    def borrar_partida(self, id_partida):
        self.get_partida(id_partida).delete_instance()

    ### EQUIPOS ###
    def get_equipos(self):
        equipos = Equipo.select()
        ret = [equipo for equipo in equipos]

        return ret

    def get_equipo(self, id_equipo):
        equipo = Equipo.get(Equipo.id == id_equipo)

        return equipo

    def crear_equipo(self, nombre, descripcion = None, valor = None,
                        id_mod = None):
        equipo = Equipo()
        equipo.nombre = nombre
        equipo.descripcion = descripcion

        if valor:
            equipo.valor = valor
        else:
            equipo.valor = 0

        if id_mod:
            mod = Mod.get(Mod.id == id_mod)
            equipo.mod = mod

        equipo.save()

        return equipo

    def editar_equipo(self, id_equipo, nombre, descripcion = None,
                        valor = None, id_mod = None):
        equipo = Equipo.get(Equipo.id == id_equipo)
        equipo.nombre = nombre
        equipo.descripcion = descripcion

        if valor:
            equipo.valor = valor
        else:
            equipo.valor = 0

        if id_mod:
            mod = Mod.get(Mod.id == id_mod)
            equipo.mod = mod

        equipo.save()
        return equipo

    def borrar_equipo(self, id_equipo):
        equipo = self.get_equipo(id_equipo)
        PlayerEquipo.delete().where(PlayerEquipo.equipo == equipo).execute()
        equipo.delete_instance()

    ### PERSONAJES ###
    def get_personajes(self, id_partida = None):
        personajes = Player.select()
        if id_partida:
            personajes = Player.select().join(Partida).where(
                            Partida.id == id_partida)
        ret = [personaje for personaje in personajes]

        return ret

    def get_personaje(self, id_personaje):
        personaje = Player.get(Player.id == id_personaje)

        return personaje

    def crear_personaje(self, datos):
        personaje = Player()

        if 'nombre' in datos:
            personaje.nombre = datos['nombre']

        if 'profesion' in datos:
            personaje.profesion = datos['profesion']

        if 'raza' in datos:
            raza = Raza.get(Raza.id == datos['raza'])
            personaje.raza = raza

        if 'pueblo' in datos:
            personaje.pueblo = datos['pueblo']

        if 'fuerza' in datos:
            personaje.fuerza = datos['fuerza']

        if 'hp' in datos:
            personaje.hp = datos['hp']
        else:
            personaje.hp = datos['fuerza'] * 5

        if 'agilidad' in datos:
            personaje.agilidad = datos['agilidad']

        if 'inteligencia' in datos:
            personaje.inteligencia = datos['inteligencia']

        if 'carisma' in datos:
            personaje.carisma = datos['carisma']

        if 'combate' in datos:
            personaje.combate = datos['combate']

        if 'conocimientos' in datos:
            personaje.conocimientos = datos['conocimientos']

        if 'latrocinio' in datos:
            personaje.latrocinio = datos['latrocinio']

        if 'magia' in datos:
            personaje.magia = datos['magia']

        if 'sociales' in datos:
            personaje.sociales = datos['sociales']

        if 'notas' in datos:
            personaje.notas = datos['notas']

        if 'partida' in datos:
            partida = Partida.get(Partida.id == datos['partida'])
            personaje.partida = partida

        personaje.save()
        return personaje

    def editar_personaje(self, id_personaje, datos):
        personaje = Player.get(Player.id == id_personaje)

        if 'nombre' in datos:
            personaje.nombre = datos['nombre']

        if 'profesion' in datos:
            personaje.profesion = datos['profesion']

        if 'raza' in datos:
            raza = Raza.get(Raza.id == datos['raza'])
            personaje.raza = raza

        if 'pueblo' in datos:
            personaje.pueblo = datos['pueblo']

        if 'fuerza' in datos:
            personaje.fuerza = datos['fuerza']

        if 'hp' in datos:
            personaje.hp = datos['hp']

        if 'agilidad' in datos:
            personaje.agilidad = datos['agilidad']

        if 'inteligencia' in datos:
            personaje.inteligencia = datos['inteligencia']

        if 'carisma' in datos:
            personaje.carisma = datos['carisma']

        if 'combate' in datos:
            personaje.combate = datos['combate']

        if 'conocimientos' in datos:
            personaje.conocimientos = datos['conocimientos']

        if 'latrocinio' in datos:
            personaje.latrocinio = datos['latrocinio']

        if 'magia' in datos:
            personaje.magia = datos['magia']

        if 'sociales' in datos:
            personaje.sociales = datos['sociales']

        if 'notas' in datos:
            personaje.notas = datos['notas']

        if 'partida' in datos:
            partida = Partida.get(Partida.id == datos['partida'])
            personaje.partida = partida

        personaje.save()
        return personaje

    def borrar_personaje(self, id_personaje):
        player = self.get_personaje(id_personaje)
        PlayerEquipo.delete().where(PlayerEquipo.player == player).execute()
        self.get_personaje(id_personaje).delete_instance()

    def get_equipos_personaje(self, id_personaje):
        equipospj = PlayerEquipo.select().join(Player)\
                    .where(Player.id == id_personaje).execute()
        ret = []
        for equipopj in equipospj:
            equipo = equipopj.equipo
            equipo.id_pj_equipo = equipopj.id
            ret.append(equipo)

        return ret

    def asignar_equipo(self, id_personaje, id_equipo):
        personaje = self.get_personaje(id_personaje)
        equipo = self.get_equipo(id_equipo)

        rel = PlayerEquipo()
        rel.player=personaje
        rel.equipo=equipo
        rel.save()

        return rel

    def borrar_equipo_pj(self, id_personaje):
        personaje = self.get_personaje(id_personaje)

        PlayerEquipo.delete().where(
            PlayerEquipo.player==personaje,
        ).execute()

    def desasignar_equipo(self, id_pj_equipo):
        PlayerEquipo.get(PlayerEquipo.id == id_pj_equipo).delete_instance()

    ### COMBOS ###
    def get_dificultad(self, id_dificultad):
        dificultad = Dificultad.get(Dificultad.id == id_dificultad)

        return dificultad

    def get_dificultades(self):
        dificultades = Dificultad.select()
        ret = [dificultad for dificultad in dificultades]

        return ret

    def get_mod(self, id_mod):
        mod = Mod.get(Mod.id == id_mod)

        return mod

    def get_mods(self):
        mods = Mod.select()
        ret = [mod for mod in mods]

        return ret

    def get_raza(self, id_raza):
        raza = Raza.get(Raza.id == id_raza)

        return raza

    def get_razas(self):
        razas = Raza.select()
        ret = [raza for raza in razas]

        return ret

    ### TIRADAS ###
    def bonus_mod_personaje(self, mod, personaje):
        pjvalue = 0

        if mod.nombre == MOD_TYPE[0][1]:   # Ataque
            pjvalue = personaje.combate
        elif mod.nombre == MOD_TYPE[1][1]: # Defensa
            pjvalue = personaje.combate
        elif mod.nombre == MOD_TYPE[2][1]: # Fuerza
            pjvalue = personaje.fuerza
        elif mod.nombre == MOD_TYPE[3][1]: # Agilidad
            pjvalue = personaje.agilidad
        elif mod.nombre == MOD_TYPE[4][1]: # Inteligencia
            pjvalue = personaje.inteligencia
        elif mod.nombre == MOD_TYPE[5][1]: # Carisma
            pjvalue = personaje.carisma
        elif mod.nombre == MOD_TYPE[6][1]: # Conocimientos
            pjvalue = personaje.conocimientos
        elif mod.nombre == MOD_TYPE[7][1]: # Latrocinio
            pjvalue = personaje.latrocinio
        elif mod.nombre == MOD_TYPE[8][1]: # Magia
            pjvalue = personaje.magia
        elif mod.nombre == MOD_TYPE[9][1]: # Sociales
            pjvalue = personaje.sociales

        return pjvalue

    def bonus_equipo_personaje(self, mod, personaje):
        equipos = Equipo.select().join(PlayerEquipo).join(Player)\
            .where(Equipo.mod == mod, PlayerEquipo.player == personaje)

        equipo_bonus = 0
        for equipo in equipos:
            equipo_bonus = equipo_bonus + equipo.valor

        return equipo_bonus

    def tirada_sin_oposicion(self, id_personaje, id_dificultad,
                                id_mod, bonus=0):
        personaje = self.get_personaje(id_personaje)
        dificultad = self.get_dificultad(id_dificultad)
        mod = Mod.get(Mod.id == id_mod)

        # obtener valor personaje
        pjvalue = self.bonus_mod_personaje(mod, personaje)

        # obtener bonus por equipo
        equipo_bonus = self.bonus_equipo_personaje(mod, personaje)

        total_bonus = bonus + equipo_bonus
        ret_tirada = self.core.sin_oposicion(pjvalue, dificultad.valor,\
                                                total_bonus)

        ret = {
            'pjvalue': pjvalue,
            'resultado': ret_tirada,
            'dado': self.core.ultimo_dado,
            'equipo_bonus': equipo_bonus,
            'dif': dificultad.valor,
        }

        return ret


    def tirada_con_oposicion(self, id_personaje, id_pnj,
                                id_mod, bonus_pj=0, bonus_pnj=0):
        personaje = self.get_personaje(id_personaje)
        adversario = self.get_personaje(id_pnj)
        mod = Mod.get(Mod.id == id_mod)

        # obtener valor personaje
        pjvalue = self.bonus_mod_personaje(mod, personaje)
        pnjvalue = self.bonus_mod_personaje(mod, adversario)

        # obtener bonus por equipo
        equipo_bonus_pj1 = self.bonus_equipo_personaje(mod, personaje)
        equipo_bonus_pnj = self.bonus_equipo_personaje(mod, adversario)

        total_bonus_pj1 = bonus_pj + equipo_bonus_pj1
        total_bonus_pnj = bonus_pnj + equipo_bonus_pnj

        ret_tirada = self.core.con_oposicion(
            pjvalue,
            pnjvalue,
            total_bonus_pj1,
            total_bonus_pnj
        )

        ret = {
            'pjvalue': pjvalue,
            'pnjvalue': pnjvalue,
            'resultado': ret_tirada,
            'dado1': self.core.dado1,
            'dado2': self.core.dado2,
            'equipo_bonus_pj1': equipo_bonus_pj1,
            'equipo_bonus_pnj': equipo_bonus_pnj,
        }

        return ret

    ### COMBATES ###
    def iniciativa(self, id_pj, id_pnj, magia=False, bonus_pj=0,
                    bonus_pnj=0):
        personaje    = self.get_personaje(id_pj)
        adversario   = self.get_personaje(id_pnj)
        mod_agilidad = Mod.get(Mod.nombre == MOD_TYPE[3][1])
        mod_magia    = Mod.get(Mod.nombre == MOD_TYPE[9][1])

        # obtener valor personaje
        pjvalue  = self.bonus_mod_personaje(mod_agilidad, personaje)
        pnjvalue = self.bonus_mod_personaje(mod_agilidad, adversario)

        magia_pjvalue  = self.bonus_mod_personaje(mod_magia, personaje)
        magia_pnjvalue = self.bonus_mod_personaje(mod_magia, adversario)

        # obtener bonus por equipo
        equipo_bonus_pj1 = self.bonus_equipo_personaje(mod_agilidad,
                                                        personaje)
        equipo_bonus_pnj = self.bonus_equipo_personaje(mod_agilidad,
                                                        adversario)
        equipom_bonus_pj1 = self.bonus_equipo_personaje(mod_magia,
                                                        personaje)
        equipom_bonus_pnj = self.bonus_equipo_personaje(mod_magia,
                                                        adversario)

        # sumamos bonus de entrada con bonus por equipo
        total_bonus_pj1 = bonus_pj + equipo_bonus_pj1
        total_bonus_pnj = bonus_pnj + equipo_bonus_pnj

        # el total de magia es el valor del pj y su equipo mágico
        total_magia_pj1 = magia_pjvalue + equipom_bonus_pj1
        total_magia_pnj = magia_pnjvalue + equipom_bonus_pnj

        ret_tirada = None

        if not magia:
            ret_tirada = self.core.iniciativa(
                pjvalue,
                pnjvalue,
                total_bonus_pj1,
                total_bonus_pnj
            )
        else:
            ret_tirada = self.core.iniciativa_m(
                pjvalue, # su valor en agilidad
                total_magia_pj1, # su valor en magia
                pnjvalue,
                total_magia_pnj,
                total_bonus_pj1, # bonus de agilidad
                total_bonus_pnj
            )

        ret = {
            'resultado': ret_tirada,
            'dado1': self.core.dado1,
            'dado2': self.core.dado2,
        }

        return ret

    def combate(self, id_pataca, id_pdefiende, magia=False,
                bonus_ata=0, bonus_def=0):
        pataca      = self.get_personaje(id_pataca)
        pdefiende   = self.get_personaje(id_pdefiende)
        mod_ataque  = Mod.get(Mod.nombre == MOD_TYPE[1][1])
        mod_defensa = Mod.get(Mod.nombre == MOD_TYPE[2][1])
        mod_magia   = Mod.get(Mod.nombre == MOD_TYPE[9][1])

        # obtener valores
        pataca_val    = self.bonus_mod_personaje(mod_ataque, pataca)
        pdefiende_val = self.bonus_mod_personaje(mod_defensa, pdefiende)

        pataca_magia    = self.bonus_mod_personaje(mod_magia, pataca)
        pdefiende_magia = self.bonus_mod_personaje(mod_magia, pdefiende)

        # obtener bonus por equipo
        equipo_bonus_pata = self.bonus_equipo_personaje(mod_ataque,
                                                        pataca)
        equipo_bonus_pdef = self.bonus_equipo_personaje(mod_defensa,
                                                        pdefiende)
        equipom_bonus_pata = self.bonus_equipo_personaje(mod_magia,
                                                        pataca)
        equipom_bonus_pdef = self.bonus_equipo_personaje(mod_magia,
                                                        pdefiende)

        total_bonus_pata = equipo_bonus_pata + bonus_ata
        total_bonus_pdef = equipo_bonus_pdef + bonus_def
        total_bonusm_pata = equipom_bonus_pata + bonus_ata
        total_bonusm_pdef = equipom_bonus_pdef + bonus_def


        ret_tirada = None

        if not magia:
            ret_tirada = self.core.combate(
                pataca_val,
                pdefiende_val,
                total_bonus_pata,
                total_bonus_pdef
            )
        else:
            ret_tirada = self.core.combatem_m(
                pataca_magia,
                pdefiende_magia,
                total_bonusm_pata,
                total_bonusm_pdef
            )

        # aplicar heridas
        herido = pdefiende

        if ret_tirada[0] != 0:
            datos = {  }

            if ret_tirada[1]: # Overkill
                datos['hp'] = 0
            elif ret_tirada[0] > 0: # heridas
                datos['hp'] = herido.hp - ret_tirada[0]
            elif ret_tirada[0] < 0: # ataque patético
                herido = pataca
                datos['hp'] = herido.hp + ret_tirada[0]

            self.editar_personaje(herido.id, datos)

        ret = {
            'resultado': ret_tirada[0],
            'overkill' : ret_tirada[1],
        }

        return ret
