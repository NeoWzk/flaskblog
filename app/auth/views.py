# encoding: utf-8
# define routes for authenticated url

from flask import render_template, redirect, url_for, flash
from app.forms import loginForm
from ..models import User
from flask_login import login_required, login_user, logout_user
from ..auth import auth


@auth.route('/login', methods=['GET', 'POST'])
def sign_in():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_pass(form.password.data):
            login_user(user)
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid credentials')
            return render_template('auth/login.html', form=form)
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('auth/dashboard.html')

