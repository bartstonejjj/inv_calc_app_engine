from datetime import datetime
from app import db, login, app
from flask_login import UserMixin
from firebase_admin import auth
from flask import url_for, redirect
from time import time
import jwt

class User(UserMixin):
    def __init__(self, user):
        self.user = user

    # Get the correct user type whether using firebase admin or pyrebase
    def resolve_user_object(self):
        user = self.user

        if type(user) == dict:
            print('dict type user')
            return user

        else:
            print('not dict type user') # For current_user
            user = user.__dict__
            return user['_data']

    def not_guest(self):
        return self.resolve_user_object()['localId'] != 0

    def get_id(self):
        return self.resolve_user_object()['localId']

    def get_email(self):
        print(self.user)
        return self.resolve_user_object()['email'] if self.not_guest() else 'Guest User'

    def get_reset_password_token(self, expires_in=600):
        token = jwt.encode(
            {'reset_password': self.get_id(), 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        # PyJWT >= 2 returns a str, so decode only if it’s bytes
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'],
            algorithms=['HS256'])['reset_password']
        except:
            return
        user = auth.get_user(user_id)
        user = user.__dict__
        user = user['_data']
        print(user)
        return user

@login.user_loader
def load_user(user_id):
    print('Loading user|', user_id, '|')
    user = auth.get_user(user_id) if user_id != 0 else {'localId':0}
    return User(user)

@login.unauthorized_handler
def authentication_required():
    print('You must login buddy...')
    return redirect(url_for('login'))