from flask import render_template, flash, redirect, send_file
from flask_login import current_user
import datetime
from flask import render_template,flash, request
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64
import matplotlib.pyplot as plt



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






### CODE RELATING TO CORRELATION
class SelectFilters(FlaskForm):
    state = SelectField("Select a state")
    issue = SelectField("Select an issue")
    candidate = SelectField("Select a candidate")
    passed = SelectField("Select passed options",choices=[("pass","pass"),("fail","fail")])
    submit = SubmitField('Filter')

class ChooseParameters(FlaskForm):
    options = SelectMultipleField("Select Selection Parameters (must select one to filter)", 
    choices=[("State","State"),("Candidate","Candidate"),("Issues","Issues"),
    ("Passed","Passed")],default = "State")
    submit = SubmitField('Select')

@bp.route('/correlation',methods=['GET', 'POST'])
def correlation():
    optionsForm = ChooseParameters()
    selectedOptions = optionsForm.options.data
    stateTruthy = False
    candidateTruthy = False
    passedTruthy = False
    issueTruthy = False

    if "State" in selectedOptions:
        stateTruthy = True
    if "Candidate" in selectedOptions:
        candidateTruthy = True
    if "Issues" in selectedOptions:
        issueTruthy = True
    if "Passed" in selectedOptions:
        passedTruthy = True    
    states = Correlation.get_unique_state()
    issues = Correlation.get_unique_issue()
    candidates = Correlation.get_unique_candidate()
    #Candidate = Correlation.get_candidate()
    choice_states = []
    choice_issues = []
    choice_candidates = []
    for s in issues:
        choice_issues.append(s.passed)
    for s in states:
        choice_states.append(s.state_id)
    for s in candidates:        
        choice_candidates.append(s.candidate_id)
    # get all correlations
    form = SelectFilters()
    form.state.choices = choice_states
    form.issue.choices = choice_issues
    form.candidate.choices = choice_candidates
    data = Correlation.get_all()
    #candidate, issue, passed, state
    if form.state.data and form.issue.data and form.passed.data and form.candidate.data:
        data = Correlation.get_passed_issue_candidate_state(form.passed.data,form.issue.data,form.candidate.data,form.state.data)
    #issue, passed, state
    elif form.state.data and form.issue.data and form.passed.data:  
        data = Correlation.get_passed_issue_state(form.passed.data,form.issue.data,form.state.data)
    #issue, state, candidate
    elif form.state.data and form.issue.data and form.candidate.data:  
        data = Correlation.get_issue_candidate_state(form.issue.data,form.candidate.data,form.state.data)
    #state, passed, candidate
    elif form.state.data and form.passed.data and form.candidate.data:  
        data = Correlation.get_passed_candidate_state(form.passed.data,form.candidate.data,form.state.data)
    #issue, passed, candidate    
    elif form.issue.data and form.passed.data and form.candidate.data:  
        data = Correlation.get_passed_issue_candidate(form.passed.data,form.issue.data,form.candidate.data)
    #issue, passed    
    elif form.issue.data and form.passed.data:
        data = Correlation.get_passed_issue(form.passed.data,form.issue.data)
    #state, passed    
    elif form.state.data and form.passed.data:
        data = Correlation.get_passed_state(form.passed.data,form.state.data)
    #candidate, passed    
    elif form.candidate.data and form.passed.data:
        data = Correlation.get_passed_candidate(form.passed.data,form.candidate.data)
    #issue, candidate    
    elif form.issue.data and form.candidate.data:
        data = Correlation.get_issue_candidate(form.issue.data,form.candidate.data)
    #issue, state    
    elif form.issue.data and form.state.data:
        data = Correlation.get_issue_state(form.issue.data,form.state.data)
    #state, candidate    
    elif form.candidate.data and form.state.data:
        data = Correlation.get_candidate_state(form.candidate.data,form.state.data)
    #state
    elif form.state.data:
            data = Correlation.get_states(form.state.data)
    #candidate        
    elif form.candidate.data:
            data = Correlation.get_candidate(form.candidate.data)
    #passed
    elif form.passed.data:
            data = Correlation.get_passed(form.passed.data)
    #issue
    elif form.issue.data:
            data = Correlation.get_issue(form.issue.data)


    #visualization component
    global x
    global y
    x = [s.issue for s in data]
    y = [float(s.committee_id) for s in data]
    img = io.BytesIO()
    y = [1,2,3,4,5]
    x = [0,2,1,3,4]

    plt.plot(x,y)
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue())

    return render_template('correlation.html',
                           data=data,
                           form = form,
                           size_choices_states = len(form.state.choices),
                           size_choices_issues = len(form.state.choices),
                           optionsForm = optionsForm,
                           stateTruthy = stateTruthy,
                           candidateTruthy = candidateTruthy,
                           passedTruthy = passedTruthy,
                           issueTruthy = issueTruthy,
                           plot_url = plot_url
            )


            
@bp.route('/visualize')
def visualize():
    fig,ax=plt.subplots(figsize=(6,6))
    ax=sns.set(style="darkgrid")
    sns.barplot(x,y)
    canvas=FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')
