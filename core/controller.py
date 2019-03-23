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
        pass
    
    def borrar_personaje(self, id_personaje):
        pass
    
    ### TIRADAS ###
    def tirada_sin_oposicion(self, id_personaje, bonus, dificultad, 
                                skill):
        pass
    
    def tirada_con_oposicion(self, id_personaje, bonuspj_, id_pnj, 
                                bonus_pnj, skill):
        pass
    
    ### COMBATES ###
    
    def iniciativa(self, id_pj, bonus_pj, id_pnj, bonus_pnj, 
                    magia=False):
        pass
    
    def combate(self, id_pataca, bonus_ata, id_pdefiende, bonus_def, 
                magia=False):
        pass
    