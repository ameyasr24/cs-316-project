from flask import render_template
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.issues import Issues
from .models.issues import Industries

from flask import Blueprint
bp = Blueprint('issues', __name__)

class SearchIssue(FlaskForm):
    issue_category = StringField('Issue')
    politician = StringField('politician')
    search = SubmitField('Search')
    

@bp.route('/issues', methods=['GET', 'POST'])
def issues():
    form = SearchIssue()

    all_issues = Issues.get_all()

    donations = Industries.get_all()

    senators = Issues.get_all_senator_names()

    subjects = Issues.get_all_subject_names()

    if form.validate_on_submit():
        all_issues = Issues.get_all_issue(form.issue_category.data)
        all_issues = Issues.get_all_issue_politician(form.issue_category.data, form.politician.data)
        donations = Industries.get_donations_senator(form.politician.data)
    return render_template('issues.html', form=form,
                           list_issues=all_issues,
                           list_donations=donations,
                           list_senators=senators,
                           list_subjects=subjects)
