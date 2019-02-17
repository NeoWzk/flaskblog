# encoding:utf-8
# create mail functions here

from . import mail
from . import create_app
from flask import render_template
from flask_mail import Message
from threading import Thread
from config import config


app = create_app(config['default'])


def async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipients, msg_template, **kwargs):
    msg = Message(subject=subject, recipients=[recipients])
    msg.html = render_template(msg_template + '.html', **kwargs)
    th = Thread(target=async_mail, args=(app, msg))
    th.start()

