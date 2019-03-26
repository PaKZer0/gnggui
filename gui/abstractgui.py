from core.controller import Controller

class AbstractGui():
    instance = None
    
    def __init__(self):
        self.con = Controller()
    
    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()
        
        return cls.instance
    
    def purge_all_data(self):
        self.con.drop_db()
    
    def exit(self):
        self.con.close_db()
    
    def run(self):
        '''
        To be implemented by subclasses
        '''
        pass
