# encoding:utf-8
# create mail functions here

from . import mail
from . import create_app
from flask import render_template
from flask_mail import Message
from threading import Thread
import os


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')


def async_mail(msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipients, msg_template, **kwargs):
    msg = Message(subject=subject, recipients=[recipients])
    msg.html = render_template(msg_template + '.html', **kwargs)
    th = Thread(target=async_mail, args=(msg,))
    th.start()
    return th

