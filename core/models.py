from peewee import *

db = SqliteDatabase('gng.db')

DIFICULTADES = [
    (2, 'Cualquiera puede hacerlo'),
    (3, 'Sencillísimo'),
    (4, 'Sencillo'),
    (5, 'Rutina'),
    (6, 'Bastante Complicado'),
    (7, 'Complicado'),
    (8, 'Muy Complicado'),
    (9, 'Algo Difícil'),
    (10, 'Difícil'),
    (11, 'Muy Difícil'),
    (12, 'Realmente Difícil'),
    (13, 'Temeridad'),
    (14, 'Locura'),
    (15, 'Absurdo'),
    (16, 'Imposible'),
]

RAZAS = [
    (1, 'Humano'),
    (2, 'Elfo'),
    (3, 'Semielfo'),
    (4, 'Enano'),
    (5, 'Halfling'),
    (6, 'Goblin'),
    (7, 'Otros'),
]

MOD_TYPE = [
    (1, 'Ataque'),
    (2, 'Defensa'),
    (3, 'Fuerza'),
    (4, 'Agilidad'),
    (5, 'Inteligencia'),
    (6, 'Carisma'),
    (7, 'Conocimientos'),
    (8, 'Latrocinio'),
    (9, 'Magia'),
    (10, 'Sociales'),
]

def init_db(test=False):
    if test:
        db = SqliteDatabase(':memory:')
    else:
        db = SqliteDatabase('gng.db', pragmas={'foreign_keys': 1})

    db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    db.connect()

    # init tables
    db.create_tables(MODELS)

    # create primitives
    try:
        r_humano = Raza.get(Raza.nombre == 'Humano')
    except:
        for raza in RAZAS:
            Raza.create(nombre=raza[1])

    try:
        mod_1 = Mod.get(Mod.nombre == 'Ataque')
    except:
        for modtype in MOD_TYPE:
            Mod.create(nombre=modtype[1])

    try:
        diff_1 = Dificultad.get(Dificultad.valor == 2)
    except:
        for dif in DIFICULTADES:
            Dificultad.create(valor=dif[0], texto=dif[1])

def drop_db():
    db.drop_tables([Partida, Dificultad, Raza, Mod, Player,
            PlayerEquipo])

def close_db():
    db.close()

class BaseModel(Model):
    class Meta:
        database = db


class Partida(BaseModel):
    nombre = CharField()
    descripcion = CharField(null = True)

    def __str__(self):
        return self.nombre


class Dificultad(BaseModel):
    valor = IntegerField()
    texto = CharField()

    def __str__(self):
        return '{} {}'.format(self.valor, self.texto)


class Raza(BaseModel):
    nombre = CharField()

    def __str__(self):
        return self.nombre


class Mod(BaseModel):
    nombre = CharField()

    def __str__(self):
        return self.nombre


class Equipo(BaseModel):
    nombre = CharField()
    descripcion = CharField(null = True)
    valor = IntegerField(null = True)
    mod = ForeignKeyField(Mod, null = True)

    def __str__(self):
        mod_txt = ''

        if self.valor > 0:
            mod_txt = ' +{} en {}'.format(
                self.valor,
                self.mod,
            )

        return '{}{}'.format(self.nombre, mod_txt)


class Player(BaseModel):
    nombre = CharField()
    profesion = CharField()
    raza = ForeignKeyField(Raza)
    pueblo = CharField(null = True)
    hp = IntegerField()
    fuerza = IntegerField()
    agilidad = IntegerField()
    inteligencia = IntegerField()
    carisma = IntegerField()
    combate = IntegerField()
    conocimientos = IntegerField()
    latrocinio = IntegerField()
    magia = IntegerField()
    sociales = IntegerField()
    notas = TextField(null = True)
    partida = ForeignKeyField(Partida)

    def __str__(self):
        return '{} | {} | {} | HP {}'.format(
            self.nombre,
            self.profesion,
            self.raza,
            self.hp,
        )


class PlayerEquipo(BaseModel):
    player = ForeignKeyField(Player)
    equipo = ForeignKeyField(Equipo)

    def __str__(self):
        return '{} | {}'.format(self.player, self.equipo)


MODELS = [Dificultad, Partida, Raza, Mod, Equipo, Player, PlayerEquipo]
