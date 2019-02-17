# encoding:utf-8
# create db models here

from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)