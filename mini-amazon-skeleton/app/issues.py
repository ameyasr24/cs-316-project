from flask import render_template
from flask_login import current_user
import datetime

from .models.issues import Issues

from flask import Blueprint
bp = Blueprint('issues', __name__)

@bp.route('/issues', methods=['GET', 'POST'])
def issues():
    all_issues = Issues.get_all()
    return render_template('issues.html',
                           list_issues=all_issues)
