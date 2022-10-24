from flask import render_template
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.issues import Issues

from flask import Blueprint
bp = Blueprint('issues', __name__)

class SearchIssue(FlaskForm):
    issue_category = StringField('Issue')
    search = SubmitField('Search')

@bp.route('/issues', methods=['GET', 'POST'])
def issues():
    form = SearchIssue()

    all_issues = Issues.get_all()

    if form.validate_on_submit():
        all_issues = Issues.get_all_issue(form.issue_category.data)
    return render_template('issues.html', form=form,
                           list_issues=all_issues)
