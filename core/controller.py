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
        
        if id_mod:
            mod = Mod.get(Mod.id == id_mod)
            equipo.mod = mod
        
        equipo.save()
        
        return equipo
    
    def editar_equipo(self, id_equipo, nombre, descripcion = None, 
                        valor = None, mod = None):
        equipo = Equipo.get(Equipo.id == id_equipo)
        equipo.nombre = nombre
        equipo.descripcion = descripcion
        equipo.valor = valor
        
        equipo.save()
        return equipo

    def borrar_equipo(self, id_equipo):
        self.get_equipo(id_equipo).delete_instance()
    
    ### PERSONAJES ###
    def get_personajes(self):
        personajes = Player.select()
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
            personaje.hp = personaje.fuerza * 5
        
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
            personaje.hp = personaje.fuerza * 5
        
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
        
        if 'partida' in datos:
            partida = Partida.get(Partida.id == datos['partida'])
            personaje.partida = partida
        
        personaje.save()
        return personaje
    
    def borrar_personaje(self, id_personaje):
        self.get_personaje(id_personaje).delete_instance()
    
    def get_equipos_personaje(self, id_personaje):
        equipos = Equipo.select().join(PlayerEquipo).join(Player)\
                    .where(Player.id == id_personaje).execute()
        ret = [equipo for equipo in equipos]
        
        return ret
    
    def asignar_equipo(self, id_personaje, id_equipo):
        personaje = self.get_personaje(id_personaje)
        equipo = self.get_equipo(id_equipo)
        
        rel = PlayerEquipo()
        rel.player=personaje
        rel.equipo=equipo
        rel.save()
    
    def robar_equipo(self, id_personaje, id_equipo):
        personaje = self.get_personaje(id_personaje)
        equipo = self.get_equipo(id_equipo)
        
        PlayerEquipo.delete().where(
            PlayerEquipo.player==personaje,
            PlayerEquipo.equipo==equipo,
        ).execute()
    
    ### COMBOS ###
    def get_dificultad(self, id_dificultad):
        dificultad = Dificultad.get(Dificultad.id == id_dificultad)
        
        return dificultad
    
    def get_dificultades(self, id_dificultad):
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
            'resultado': ret_tirada,
            'dado': self.core.ultimo_dado,
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
            'resultado': ret_tirada,
            'dado1': self.core.dado1,
            'dado2': self.core.dado2,
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
        
        
        total_bonus_pj1 = bonus_pj + equipo_bonus_pj1
        total_bonus_pnj = bonus_pnj + equipo_bonus_pnj
        
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
                pjvalue, 
                total_magia_pj1, 
                pnjvalue, 
                total_magia_pnj, 
                total_bonus_pj1, 
                total_bonus_pnj
            )
        
        ret = {
            'resultado': ret_tirada,
            'dado1': self.core.dado1,
            'dado2': self.core.dado2,
        }
        
        return ret
    
    def combate(self, id_pataca, bonus_ata, id_pdefiende, bonus_def, 
                magia=False):
        pass
    
