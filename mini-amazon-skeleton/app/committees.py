from flask import render_template
from flask_login import current_user
import datetime

from .models.committees import Committee


from flask import Blueprint
bp = Blueprint('committee', __name__)

@bp.route('/committee', methods=['GET', 'POST'])
def committee():
    committees = Committee.get_all(True)
    print(committees)
    print("hey")
    return render_template('committees.html',
                           all_committees=committees)

# @bp.route('/committee')
# def committees():
#     # get all committees:
#     committees = Committee.get_all(True)
#     return render_template('committees.html',
#                            all_committees=committees)
