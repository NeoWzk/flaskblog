# encoding: utf-8
# create main Blueprint here

from flask import Blueprint
main = Blueprint('main', __name__)
from . import views