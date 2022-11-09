from flask import render_template, flash, redirect
from flask_login import current_user
import datetime
from flask import render_template,flash, request
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.product import Product
from .models.purchase import Purchase

from .models.states import State
from .models.candidates import Candidate_Vote
from .models.correlation import Correlation


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
    congresses = Candidate_Vote.get_all_congresses(cid)
    votetypes = Candidate_Vote.get_all_vote_types(cid)
    voteyears = Candidate_Vote.get_all_vote_years(cid)
    if votes == "oops":
        flash('There are no voting records for Senator with id ' + cid)
    return render_template('/candidate.html',
                            all_votes = votes,
                            all_congresses = congresses,
                            all_vote_types = votetypes,
                            all_vote_years = voteyears,
                            cid = cid)
@bp.route('/candidate/<cid>/congress/<congress>', methods=['GET', 'POST'])
def candidatecongressfilt(cid, congress):
    votes = Candidate_Vote.get_all_votes_for_congress(cid, congress)
    congresses = Candidate_Vote.get_all_congresses(cid)
    if votes == "oops":
        flash('There are no voting records for Senator with id ' + cid + ' and congress ' + congress)
    return render_template('/candidatecongressfilt.html',
                            all_votes = votes,
                            cid = cid,
                            all_congresses = congresses,
                            congress = congress)

@bp.route('/candidate/<cid>/votetype/<votetype>', methods=['GET', 'POST'])
def candidatevotetypefilt(cid, votetype):
    votes = Candidate_Vote.get_all_votes_for_votetype(cid, votetype)
    votetypes = Candidate_Vote.get_all_vote_types(cid)
    if votes == "oops":
        flash('There are no voting records for Senator with id ' + cid + ' and vote ' + votetype)
    return render_template('/candidatevotetypefilt.html',
                            all_votes = votes,
                            cid = cid,
                            all_vote_types = votetypes,
                            votetype = votetype)

@bp.route('/candidate/<cid>/voteyear/<voteyear>', methods=['GET', 'POST'])
def candidatevoteyearfilt(cid, voteyear):
    votes = Candidate_Vote.get_all_votes_for_voteyear(cid, voteyear)
    voteyears = Candidate_Vote.get_all_vote_years(cid)
    if votes == "oops":
        flash('There are no voting records for Senator with id ' + cid + ' and year ' + year)
    return render_template('/candidatevoteyearfilt.html',
                            all_votes = votes,
                            cid = cid,
                            all_vote_years = voteyears,
                            voteyear = voteyear)

@bp.route('/candidate/', methods=['GET', 'POST'])
def candidatehomepage():
    names = Candidate_Vote.get_all_candidates()
    if names == "oops":
        flash('There are no candidates in the data')
    candidate_name = request.args.get('name_candidate_search')
    candidate_icpsr = 0
    for name in names:
        if name[0] == candidate_name:
            candidate_icpsr = name[1]
            break
    if candidate_icpsr != 0:
        candidate_page = "/candidate/" + str(candidate_icpsr)
        return redirect(candidate_page, code=302)
    return render_template('/candidatehomepage.html', all_names=names)

class SelectStates(FlaskForm):
    state = SelectField("Select a state")
    issue = SelectField("Select an donator")
    submit = SubmitField('Submit')


@bp.route('/correlation',methods=['GET', 'POST'])
def correlation():
    states = Correlation.get_unique_state()
    issues = Correlation.get_unique_issue()
    choice_states = []
    choice_issues = []
    for s in issues:
        choice_issues.append(s.issue)
    for s in states:
        choice_states.append(s.state_id)
    # get all correlations
    form = SelectStates()
    form.state.choices = choice_states
    form.issue.choices = choice_issues
    data = Correlation.get_all()
    if form.validate_on_submit():
        data = Correlation.get_states(form.state.data)
    return render_template('correlation.html',
                           data=data,
                           form = form,
                           size_choices_states = len(form.state.choices),
                           size_choices_issues = len(form.state.choices)
            )

