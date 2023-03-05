
import hashlib
from flaskr.backend import Backend 

class User:
    def __init__(self, username):
        self. username = username
        # self. password = hashlib.blake2b(password.encode()).hexdigest()
        # self. backend = backend

    def is_authenticated(self):
        #return self.backend.sign_in(self.username, self.password)
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return f"{self.username}"

