from flask import render_template
from flask_login import current_user
import datetime

from .models.committees import Committees


from flask import Blueprint
bp = Blueprint('committees', __name__)

@bp.route('/committee', methods=['GET', 'POST'])
def committees():
    comms = Committees.get_all()
    return render_template('committees.html',
                           all_committees=comms)

