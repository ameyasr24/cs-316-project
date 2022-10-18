from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from flask import Blueprint
bp = Blueprint('comms', __name__)


class Committees:
    def __init__(self, id, from_entity, to_entity,donation_amount,from_category,to_category, year):
        self.id = id
        self.from_entity = from_entity
        self.to_entity = to_entity
        self.donation_amount = donation_amount
        self.from_category=from_category
        self.to_category=to_category
        self.year = year

    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, from_entity, to_entity, donation_amount, from_category, to_category, year
            FROM Committees
            WHERE id = :id
            ''',
                            id=id)
        return Committees(*(rows[0])) if rows else None

    @staticmethod
    def get_all_to_entity(to_entity):
        rows = app.db.execute('''
            SELECT id, from_entity, year, donation_amount
            FROM Committees
            WHERE to_entity = :to_entity
            ORDER BY year DESC
            ''',
                              to_entity=to_entity,
                              )
        return [Committees(*row) for row in rows]
    @staticmethod
    def get_all_to_entity_from(to_entity, from_date):
        rows = app.db.execute('''
            SELECT id, from_entity, year, donation_amount
            FROM Committees
            WHERE to_entity = :to_entity
            AND year>=:from_date
            ORDER BY year DESC
            ''',
                              to_entity=to_entity,
                              from_date=from_date
                              )
        return [Committees(*row) for row in rows]
    @staticmethod
    def get_all_to_entity_from_to(to_entity, from_date, to_date):
        rows = app.db.execute('''
            SELECT id, from_entity, year, donation_amount
            FROM Committees
            WHERE to_entry = :to_entity
            AND year>=:from_date AND year<=:to_date
            ORDER BY year DESC
            ''',
                              to_entity=to_entity,
                              from_date=from_date,
                              to_date=to_date
                              )
        return [Committees(*row) for row in rows]
    @staticmethod
    def get_all_from_entity(from_entity):
       rows = app.db.execute('''
            SELECT id, from_entity, year, donation_amount
            FROM Committees
            WHERE from_entity = :from_entity
            ORDER BY year DESC
            ''',
                              from_entity=from_entity,
                              )
        return [Committees(*row) for row in rows]




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
class SearchCommittee(FlaskForm):
    search_value = StringField('Senator Name', validators=[DataRequired()])
    type_senator = BooleanField('senator')
    type_committee = BooleanField('committee')
    from_year = StringField('From Year (default is all time)', default=0)
    to_year = StringField('To Year', default=2022)
    search = SubmitField('Search')
@bp.route('/committee', methods=['GET', 'POST'])
def committee():
    form = SearchCommittee()
    if form.validate_on_submit():
        
    return render_template('committees.html')
 

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


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))
