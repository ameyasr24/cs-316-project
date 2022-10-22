from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from .models.states import State


from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/state/<state_abb>', methods=['GET', 'POST'])
def state(state_abb):
    state = State.get_all(state_abb)
    return render_template('/states.html',
                            all_states = state)


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
    users = User.get_all(True)
    return render_template('index.html',
                           avail_products=products,

                           purchase_history=purchases)

