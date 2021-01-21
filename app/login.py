from flask_login import UserMixin, LoginManager



login_manager = LoginManager()



class Logger(UserMixin):


    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active




    def is_active(self):
        return self.active




    def is_anonymous(self):
        return False




    def is_authentificated(self):
        return True
