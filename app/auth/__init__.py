# encoding: utf-8
# create authentication blueprint here

from flask import Blueprint
auth = Blueprint('auth', __name__)
from . import views
