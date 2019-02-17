# encoding: utf-8
# basic config settings here

import os


class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class devconfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.getcwd() + '/dev.db'


class testconfig(config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.getcwd() + '/test.db'


class production_config(config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(os.environ.get('DB_USER'),
                                                                      os.environ.get('DB_PASS'),
                                                                      os.environ.get('DB_HOST'),
                                                                      os.environ.get('DB_PORT'),
                                                                      os.environ.get('DB_TABLE'))


config = {
    'development': devconfig,
    'test': testconfig,
    'production_config': production_config,
    'default': devconfig
}