# encoding: utf-8
# define routes here

from flask import render_template, redirect, url_for, flash
from ..main import main
from ..forms import signupForm
from .. import db
from ..models import User
from ..mails import send_mail


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = signupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.email == form.email.data:
            flash('Username and email already taken!')
            return redirect(url_for('auth.sign_in'))
        else:
            user = User(username=form.username.data, email=form.email.data, password=form.confirm.data)
            db.session.add(user)
            db.session.commit()
            send_mail('New User Just Joined', '2585414795@qq.com', 'mail/new_user', user=user.username)
            flash('congrats! You\'re successfully registered')
    return render_template('register.html', form=form)

