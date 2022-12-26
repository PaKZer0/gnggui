from core.controller import Controller

class AbstractGui():
    instance = None

    def __init__(self, test=False, db_instance=None):
        self.con = Controller(test=test, db_instance=db_instance)
        self.is_test = test

    @classmethod
    def get_instance(cls, test=False, db_instance=None):
        if not cls.instance:
            cls.instance = cls(test=test, db_instance=db_instance)

        return cls.instance

    @classmethod
    def get_controller(cls):
        return cls.get_instance().con

    def purge_all_data(self):
        self.con.drop_db()

    def exit(self):
        self.con.close_db()

    def run(self):
        '''
        To be implemented by subclasses
        '''
        pass
    
    def build_native(self):
        '''
        To be implemented by subclasses
        '''
        pass
    
    def build_option_list(self, abstract_list, str_attr, option_name, 
        with_empty=False, self_iters=None):
        '''
        To be implemented by subclasses
        '''
        pass

    def load_combo(self, option_list):
        '''
        To be implemented by subclasses
        '''
        pass
    
    def load_partidas_combo(self):
        partidas = self.con.get_partidas()
        partidas_list = self.build_option_list(partidas, 'id', 'nombre', 'partida')
        self.load_combo(partidas_list, 'combo-partida')
    
    def load_mods_equipo_combo(self):
        mods = self.con.get_mods()
        mods_list = self.build_option_list(
            mods, 'id', 'nombre', 'mod', True, 'eqmod_iters')
        self.load_combo(mods_list, 'combo-equipo-mod')
    
    def load_mods_tirada_combo(self):
        mods = self.con.get_mods()
        mods_list = self.build_option_list(mods, 'id', 'nombre', 'mod')
        self.load_combo(mods_list, 'combo-mod-tirada')
    
    def load_mods_combo(self):
        self.load_mods_equipo_combo()
        self.load_mods_tirada_combo()
    
    def load_razas_combo(self):
        razas = self.con.get_razas()
        razas_list = self.build_option_list(
            razas, 'id', 'nombre', 'raza', False, 'pjraza_iters')
        self.load_combo(razas_list, 'combo-personaje-raza')
    
    def load_equipos_combo_gen(self, id_combo):
        def fmt_func(item):
            texto_mod = ''
            if item.mod:
                if item.valor > 0:
                    texto_mod = f' +{item.valor} en {item.mod.nombre}'
                elif item.valor <= 0:
                    texto_mod = f' {item.valor} en {item.mod.nombre}'

            return f'{item.nombre}{texto_mod}'
        
        equipos = self.con.get_equipos()
        equipos_list = self.build_fmt_option_list(
            equipos, 'id', fmt_func, 'equipo', True, 'pjequi_iters')
        self.load_combo(equipos_list, id_combo)
    
    def load_equipos_pj_combo(self):
        self.load_equipos_combo_gen('combo-personaje-equipo')
    
    def load_equipos_asociado_combo(self):
        self.load_equipos_combo_gen('combo-equipo-asociado')
    
    def load_equipos_combo(self):
        self.load_equipos_pj_combo()
        self.load_equipos_asociado_combo()
    
    def build(self):
        '''
        Builds the basic gui
        '''
        # build specific gui code
        self.build_native()

        # cargar combos
        self.load_partidas_combo()
        self.load_mods_combo()
        self.load_razas_combo()
        self.load_equipos_combo()
        self.load_dificultades_combo()

        # load spinners
        self.load_spiners()

        # cargar lista equipo
        self.load_list_equipo()

        # set vars
        self.partida             = None
        self.id_personaje_sel    = None
        self.id_pj_ini           = None
        self.id_pnj_ini          = None
        self.id_pj_ataca         = None
        self.id_pj_defiende      = None
        self.ataca_pj            = None
        self.bt_asignar_activado = False
        self.bt_reset_activado   = False
        self.check_magia_ini     = False
        self.check_magia_com     = False
