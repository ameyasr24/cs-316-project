from flask import render_template,flash
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from .models.correlation import Correlation

from flask import Blueprint
bp = Blueprint('correlation',__name__)


@bp.route('/correlation')
def correlation():
    # get all available products for sale:
    data = Correlation.get_all()
    # find the products current user has bought:
    # render the page by adding information to the index.html file
    return render_template('correlation.html',
                           data=data)
