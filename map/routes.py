import os
import secrets

from flask import render_template, url_for, flash, redirect, request, abort
from map import app, db, bcrypt
from map.forms import RegistrationForm, LoginForm
from map.models import User
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return  render_template("map.html")
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Hesab uğurla yaradıldı. Hesaba giriş edə bilərsiniz!', 'success')
        return redirect(url_for('login'))


    return render_template('register.html', title='Register', form=form)


    return render_template('register.html', form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return  render_template("map.html")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return render_template("map.html")
        else:
            flash('Hasaba daxil olmaq mumkun olmadi. Daxil etdiyiniz Email ve Kodu tekrar yoxlayin!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))