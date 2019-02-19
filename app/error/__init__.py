# encoding: utf-8
# create error blueprint here

from flask import Blueprint
error = Blueprint('error', __name__)

from . import views