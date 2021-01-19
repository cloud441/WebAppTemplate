from flask import session, g


from database.db import get_db


class Logger():


    def __init__(self):
        self.logged = False


    @staticmethod
    def loadLoggedUser():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = get_db().execute(
                'SELECT * FROM user WHERE id = ?', (user_id,)
            ).fetchone()




    def login_user(self, user):

        session.clear()
        session['user_id'] = user['id']
        self.logged = True




    def logout_user(self):
        session.clear()
        self.logged = False




    def is_logged(self):
        return self.logged


logger = Logger()
