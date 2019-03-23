import random

class Core():
    """
    Clase para realizar cálculos básicos de G&G
    """
    def dado(self):
        """
        Tira un dado y almacen al resultado
        
        :returns: resultado entre 1 y 8
        """
        self.ultimo_dado = random.randint(1, 8)
        return self.ultimo_dado
    
    # tirada sin oposición
    
    def sin_oposicion(self, pjvalue, dificultad, mod=0):
        """
        Habilidad  o  Característica  +  1d8  >  Dificultad  =
        Éxito.
        Habilidad o Característica + 1d8 <
        Dificultad = Fracaso.

        :param pjvalue: el valor del personaje
        :param mod: modificador
        :param dificultad: 
        :returns: boolean si la acción ha tenido éxito
        """
        while True:
            if (pjvalue + mod + self.dado()) > dificultad:
                return True
            if (pjvalue + mod + self.dado()) < dificultad:
                return False
    
    # tirada con oposición
    def con_oposicion(self, pjvalue, vsvalue, pjmod=0, vsmod=0):
        """
        Compara dos tiradas de:
        Puntuación de la habilidad o Característica + 1d8

        :param pjvalue: el valor del personaje
        :param vsvalue: el valor del adversario
        :param pjmod: mod del jugador
        :param vsmod: mod del adversario
        :returns: boolean si el pj ha tenido éxito
        """
        while True:
            self.dado1 = self.dado()
            self.dado2 = self.dado()
            
            resultadopj = pjvalue + self.dado1 + pjmod
            resultadovs = vsvalue + self.dado2 + vsmod
            
            if resultadopj > resultadovs:
                return True
            if resultadopj < resultadovs:
                return False
    
    # iniciativa
    def iniciativa(self, agilidad1, agilidad2, mod1=0, mod2=0):
        """
        Agilidad + 1d8

        :param agilidad1: 
        :param agilidad2: 
        :returns: True si empieza jugador 1
        """
        while True:
            self.dado1 = self.dado()
            self.dado2 = self.dado()
            
            respj1 = agilidad1 + self.dado1 + mod1
            respj2 = agilidad2 + self.dado2 + mod2
            
            if respj1 > respj2:
                return True
            if respj1 < respj2:
                return False
    
    # combate
    def combate(self, ataque1, defensa2, mod1=0, mod2=0):
        """
        Puntuación del combate/ataque del atacante
        +  1d8  -(Puntuación  de  combate/defensa  del
        defensor + 1d8) = Puntos de vida perdidos
        del defensor.

        :param ataque1: ataque atacante
        :param defensa2: defensa defensor
        :param mod1: modificador atacante
        :param mod2: modificador defensor
        :returns: tupla con resultado combate y golpe certero
        """
        overkill = False
        self.dado1 = self.dado()
        self.dado2 = self.dado()
        
        d1 = self.dado1
        d2 = 0
        
        if d1 == 8:
            d2 = self.dado()
            self.dado1 = d1 + d2
        
        if d2 == 8:
            overkill = True
        
        respj1 = ataque1  + self.dado1 + mod1
        respj2 = defensa2 + self.dado2 + mod2
        
        res = respj1 - respj2
        
        return res, overkill
    
    # iniciativa mágica
    def iniciativa_m(self, agilidad1, magia1, agilidad2, magia2, mod1=0, mod2=0):
        """
        Magia + Agilidad + 1d8

        :param agilidad1: 
        :param agilidad2: 
        :returns: True si empieza jugador 1
        """
        while True:
            self.dado1 = self.dado()
            self.dado2 = self.dado()
            
            respj1 = agilidad1 + magia1 + self.dado1 + mod1
            respj2 = agilidad2 + magia2 + self.dado2 + mod2
            
            if respj1 > respj2:
                return True
            if respj1 < respj2:
                return False
    
    # combate mágico
    def combatem_m(self, magia1, magia2, mod1=0, mod2=0):
        """
        Puntuación del combate/ataque del atacante
        +  1d8  -(Puntuación  de  combate/defensa  del
        defensor + 1d8) = Puntos de vida perdidos
        del defensor.

        :param magia1: magia atacante
        :param magia2: magia defensor
        :param mod1: modificador atacante
        :param mod2: modificador defensor
        :returns: tupla con resultado combate y golpe certero
        """
        overkill = False
        self.dado1 = self.dado()
        self.dado2 = self.dado()
        
        d1 = self.dado1
        d2 = 0
        
        if d1 == 8:
            d2 = self.dado()
            self.dado1 = d1 + d2
        
        if d2 == 8:
            overkill = True
        
        respj1 = magia1  + self.dado1 + mod1
        respj2 = magia2 + self.dado2 + mod2
        
        res = respj1 - respj2
        
        return res, overkill