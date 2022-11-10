from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User

from flask import Blueprint
bp = Blueprint('users', __name__)

#move these to respective python files later


    
@bp.route('/candidate', methods=['GET', 'POST'])
def candidate():
    
    return render_template('candidate.html')
@bp.route('/correlation', methods=['GET', 'POST'])
def correlation():
    
    return render_template('correlation.html')
    
@bp.route('/issue', methods=['GET', 'POST'])
def issue():
    return render_template('issue.html')
@bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)