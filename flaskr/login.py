# It looks like we don't use these imports. It's good to avoid importing things
# you don't need. There are performance implications for unneeded imports, but
# it can also confuse the reader.
from flask_login import LoginManager, login_user
import hashlib
from flaskr.backend import Backend


#Creating a user class to represent users
class User:
    def __init__(self, username):
        self. username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return f"{self.username}"


