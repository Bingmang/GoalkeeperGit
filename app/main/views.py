from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import main
from .. import db
from ..models import User, Permission
from ..email import send_email


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('goalkeeper.html')


@main.route('/index2', methods=['GET', 'POST'])
def index2():
    return render_template('cloud.html')


@main.route('/jizu', methods=['GET', 'POST'])
def jizu():
    return render_template('jizufuxi.html')


@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')