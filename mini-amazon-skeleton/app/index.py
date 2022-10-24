from flask import render_template, flash
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from .models.states import State
from .models.candidates import Candidate_Vote


from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/state/<state_abb>', methods=['GET', 'POST'])
def state(state_abb):
    state = State.get_all(state_abb)
    return render_template('/states.html',
                            all_states = state)

@bp.route('/candidate/<cid>', methods=['GET', 'POST'])
def candidate(cid):
    votes = Candidate_Vote.get_all_votes(cid)
    if votes == "oops":
        flash('There are no voting records for Senator with id ' + cid)
    return render_template('/candidate.html',
                            all_votes = votes)

@bp.route('/candidate/', methods=['GET', 'POST'])
def candidatehomepage():
    names = Candidate_Vote.get_all_candidates()
    if names == "oops":
        flash('There are no candidates in the data')
    return render_template('/candidatehomepage.html',
                            all_names = names)

@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,

                           purchase_history=purchases)

