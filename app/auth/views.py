# encoding: utf-8
# define routes for authenticated url

from flask import render_template, redirect, url_for, flash, request
from app.forms import signupForm, loginForm, profileForm
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
        flash('A confirmation email has been sent to your email')
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def email_confirmation(token):
    if current_user.confirmed:
        flash('Email already confirmed!')
        return redirect(url_for('main.index'))
    else:
        if current_user.confirm_token(token):
            flash('Your email confirmed successfully!')
        else:
            flash('Invalid or expired token!')
        return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def sign_in():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_pass(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('auth.sign_in'))
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


@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(email=current_user.email).first()
    data = {
        'username': user.username,
        'email': user.email,
    }
    return render_template('auth/account.html', data=data)


@auth.route('/account/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = profileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        username = form.username.data
        email = form.email.data
        password = form.confirm.data
        user.username = username
        user.email = email
        user.password = password
        db.session.add(user)
        db.session.commit()
        flash('Account Details Changed!')
        send_mail('Account Details Updated', user.email, 'mail/info_update', user=user.username)
        return redirect(url_for('auth.account'))
    return render_template('auth/edit_profile.html', form=form)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and \
            current_user.confirmed is not True and \
            request.endpoint[:5] != 'auth.' and \
            request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    return render_template('unconfirmed.html')


@auth.route('/resend_confirm_msg')
@login_required
def resend_confirm_msg():
    if current_user.is_authenticated:
        token = current_user.generate_confirm_token()
        send_mail('Email Confirmation Needed',
                  current_user.email,
                  'confirm/user_confirm',
                  user=current_user.username,
                  token=token)
        send_mail('Confirmation Msg Resent', '2585414795@qq.com', 'confirm/resend_confirm')
        flash('Confirmation Message have been resent successfully!')
    return render_template('unconfirmed.html')
