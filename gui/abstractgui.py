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
