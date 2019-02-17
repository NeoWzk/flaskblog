# encoding: utf-8
# define routes here

from flask import render_template, redirect, url_for, flash
from ..main import main
from ..forms import signupForm
from app.models import User, db


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/register', methods=['GET', 'POST'])
def user_register():
    form = signupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already taken!')
            if user.email == form.email.data:
                flash('Email Add already registered')
                return render_template('register.html', form=form)
        else:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.sign_in'))
    return render_template('register.html', form=form)
