import bcrypt
import re
import base64

import flask
import os
import models
import math

from models import Pet
from models import User
from init import db, app
from datetime import datetime, date
from dateutil import relativedelta


@app.route('/')
def landing():
    return flask.render_template('landing.html')


@app.route('/home')
def home():
    return flask.render_template('home.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    form_date = flask.request.form['pet-age']
    pet_age = form_date.replace('-', ' ')
    date_of_birth = datetime.strptime(pet_age, "%Y %m %d")
    total_age = calculate_total(date_of_birth)
    total_days = calculate_days(date_of_birth)
    total_weeks = calculate_weeks(date_of_birth)
    return flask.render_template('age.html', total_age=total_age, total_days=total_days, total_weeks=total_weeks)


@app.route('/login')
def login_page():
    return flask.render_template('login.html')


@app.route('/signup')
def handle_signup():
    return flask.render_template('signup.html')


@app.route('/login', methods=['POST'])
def handle_login():
    login = flask.request.form['user']
    password = flask.request.form['password']

    # find user
    user = models.User.query.filter_by(login=login).first()
    if user is not None:
        pw_hash = bcrypt.hashpw(password.encode('utf8'), user.pw_hash)
        # compare passwords
        if pw_hash == user.pw_hash:
            flask.session['auth_user'] = user.id
            return flask.redirect('/home', code=303)

    return flask.render_template('signup.html', error='Invalid username or password')


@app.route('/create', methods=['POST'])
def create_user():
    email = flask.request.form['email']
    login = flask.request.form['user']
    password = flask.request.form['password']

    error = None

    if password != flask.request.form['confirm-password']:
        error = "Passwords don't match"
        print("Passwords don't match")

    if not re.search("^[A-Za-z0-9_-]*$", login):
        error = "Username can only contain letters, numbers, underscore, hyphen"
        print("Username typing error")

    existing = models.User.query.filter_by(login=login).first()
    if existing is not None:
        error = "Username already exists"
        print("Username already exists")

    if error:
        return flask.render_template('signup.html', error=error)

    # add user to database
    user = models.User()
    user.login = login
    user.email = email
    user.pw_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(15))

    db.session.add(user)
    db.session.commit()
    flask.session['auth_user'] = user.id
    return flask.redirect(flask.url_for('home'), 303)


def calculate_total(born):
    today = date.today()
    r = relativedelta.relativedelta(today, born)
    #print("Total age: " + str(r.years) + " years " + str(r.months) + " months " + str(r.days) + " days")
    return r


def calculate_days(born):
    # Calculate total number of days born
    days = date.today()-date(born.year, born.month, born.day)
    #print("Days: " + str(days.days))
    return days


def calculate_weeks(born):
    # Calculate total number of weeks
    days = date.today() - date(born.year, born.month, born.day)
    weeks = math.floor(days.days / 7)
    #print("Weeks: " + str(weeks))
    return weeks
