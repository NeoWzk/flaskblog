# encoding:utf-8
# create db models here

from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from flask import current_app


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_pass(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # function for generating token
    def generate_confirm_token(self, expiration=3600):
        s = serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        token = s.dumps({'confirm': self.id})
        return token

    # function for decode token and update table
    def confirm_token(self, token):
        s = serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            if data.get('confirm') != self.id:
                return False
            else:
                self.confirmed = True
                db.session.add(self)
                db.session.commit()
                return True
        except:
            return False

    def __repf__(self):
        return 'User {}'.format(self.username)
