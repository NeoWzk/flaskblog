from flask import render_template, url_for, redirect, flash
from . import error


@error.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')


@error.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html')


@error.app_errorhandler(401)
def unauthorized(e):
    return render_template('errors/unauthorized.html')