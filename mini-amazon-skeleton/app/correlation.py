from flask import render_template,flash
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from .models.correlation import Correlation

from flask import Blueprint
bp = Blueprint('correlation',__name__)


@bp.route('/correlation',methods=['GET', 'POST'])
def correlation():
    # get all correlations
    data = Correlation.get_all()
    apples = "apple"
    print(data)
    print("hello")
    return render_template('correlation.html',
                           data=data,
                           apple = apples)
