from flask_login import LoginManager, login_user
import hashlib
from flaskr.backend import Backend
from flaskr.settings import Settings


#Creating a user class to represent users
class User:

    def __init__(self, username):
        self.username = username
        self.settings = Settings()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return f"{self.username}"
