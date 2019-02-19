# encoding: utf-8
# define routes for authenticated url

from flask import render_template, redirect, url_for, flash
from app.forms import signupForm, loginForm
from ..models import User
from flask_login import login_required, login_user, logout_user, current_user
from ..auth import auth
from ..mails import send_mail
from app import db


@auth.route('/register', methods=['GET', 'POST'])
def user_register():
    form = signupForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(username=form.username.data).first()
        # if user:
        #     flash('Username and email already taken!')
        #     return redirect(url_for('auth.sign_in'))
        # else:
        #     user = User(username=form.username.data, email=form.email.data, password=form.confirm.data)
        #     db.session.add(user)
        #     db.session.commit()
        #     send_mail('New User Just Joined', '2585414795@qq.com', 'mail/new_user', user=user.username)
        #     flash('congrats! You\'re successfully registered')
        # before adding validate_username and validate_email functions
        # after adding 'validate_' functions
        user = User(username=form.username.data, email=form.email.data, password=form.confirm.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirm_token(expiration=3600)
        send_mail('Please confirm your email asap!', user.email, 'confirm/user_confirm', user=user.username, token=token)
        send_mail('New User Just Joined', '2585414795@qq.com', 'mail/new_user', user=user.username)
        flash('One more step needed! A confirmation mail has been sent to your email!')
    return render_template('register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirm:
        flash('Your details already confirmed!')
        return redirect(url_for('main.index'))
    else:
        if current_user.confirm_token(token):
            flash('Congrats! Your Email Confirmed!')
            login_user(current_user)
            return redirect(url_for('auth.dashboard'))
        else:
            err = 'Error:Token invalid or expired!'
            return render_template('errors/customerr.html', err=err)


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

