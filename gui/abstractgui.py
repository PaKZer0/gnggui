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
        mods_list = self.build_option_list(mods, 'id', 'nombre', 'mod', True, 'eqmod_iters')
        self.load_combo(mods_list, 'combo-equipo-mod')
    
    def load_mods_tirada_combo(self):
        mods = self.con.get_mods()
        mods_list = self.build_option_list(mods, 'id', 'nombre', 'mod')
        self.load_combo(mods_list, 'combo-mod-tirada')
    
    def build(self):
        '''
        Builds the basic gui
        '''
        # build specific gui code
        self.build_native()

        # cargar combos
        self.load_partidas_combo()
        self.load_mods_combo()
        #self.load_mods_equipo_combo()
        #self.load_mods_tirada_combo()
        self.load_razas_combo()
        self.load_equipos_combo()
        self.load_dificultades_combo()
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
