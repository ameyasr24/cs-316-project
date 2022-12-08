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
import numpy as np
from flask_paginate import Pagination, get_page_parameter



from .models.states import State
# from .models.states import Year
from .models.candidates import Candidate_Vote
from .models.candidates import Candidate_Donations
from .models.correlation import Correlation


from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/state/<state_abb>', methods=['GET', 'POST'])
def state(state_abb):
    state = State.get_all(state_abb)
    year = State.get_unique_years(state_abb)
    return render_template('/states.html',
                            all_states = state,
                            all_years = year)
                            # ,all_years = year)


@bp.route('/state/<state_abb>/<year>/', methods=['GET', 'POST'])
def staterace(state_abb, year):
    race = State.get_all_year(state_abb, year)
    return render_template('/staterace.html',
                            all_race = race)

@bp.route('/candidate/<cid>', methods=['GET', 'POST'])
def candidate(cid):
    votes = Candidate_Vote.get_all_votes(cid)
    congresses = Candidate_Vote.get_all_congresses(cid)
    votetypes = Candidate_Vote.get_all_vote_types(cid)
    voteyears = Candidate_Vote.get_all_vote_years(cid)
    donations = Candidate_Donations.get_all_donations(cid)
    grouped_don = Candidate_Donations.grouped_donations(cid)
    if votes == "oops":
        flash('There are no voting records for Senator with id ' + cid)
    return render_template('/candidate.html',
                            all_votes = votes,
                            all_congresses = congresses,
                            all_vote_types = votetypes,
                            all_vote_years = voteyears,
                            cid = cid,
                            all_donations = donations,
                            grouped_donations = grouped_don)
@bp.route('/candidate/<cid>/congress/<congress>', methods=['GET', 'POST'])
def candidatecongressfilt(cid, congress):
    votes = Candidate_Vote.get_all_votes_for_congress(cid, congress)
    congresses = Candidate_Vote.get_all_congresses(cid)
    donations = Candidate_Donations.get_all_donations(cid)
    grouped_don = Candidate_Donations.grouped_donations(cid)
    if votes == "oops":
        flash('There are no voting records for Senator with id ' + cid + ' and congress ' + congress)
    return render_template('/candidatecongressfilt.html',
                            all_votes = votes,
                            cid = cid,
                            all_congresses = congresses,
                            congress = congress,
                            all_donations = donations,
                            grouped_donations = grouped_don)

@bp.route('/candidate/<cid>/votetype/<votetype>', methods=['GET', 'POST'])
def candidatevotetypefilt(cid, votetype):
    votes = Candidate_Vote.get_all_votes_for_votetype(cid, votetype)
    votetypes = Candidate_Vote.get_all_vote_types(cid)
    donations = Candidate_Donations.get_all_donations(cid)
    grouped_don = Candidate_Donations.grouped_donations(cid)
    if votes == "oops":
        flash('There are no voting records for Senator with id ' + cid + ' and vote ' + votetype)
    return render_template('/candidatevotetypefilt.html',
                            all_votes = votes,
                            cid = cid,
                            all_vote_types = votetypes,
                            votetype = votetype,
                            all_donations = donations,
                            grouped_donations = grouped_don)

@bp.route('/candidate/<cid>/voteyear/<voteyear>', methods=['GET', 'POST'])
def candidatevoteyearfilt(cid, voteyear):
    votes = Candidate_Vote.get_all_votes_for_voteyear(cid, voteyear)
    voteyears = Candidate_Vote.get_all_vote_years(cid)
    donations = Candidate_Donations.get_all_donations(cid)
    grouped_don = Candidate_Donations.grouped_donations(cid)
    if votes == "oops":
        flash('There are no voting records for Senator with id ' + cid + ' and year ' + year)
    return render_template('/candidatevoteyearfilt.html',
                            all_votes = votes,
                            cid = cid,
                            all_vote_years = voteyears,
                            voteyear = voteyear,
                            all_donations = donations,
                            grouped_donations = grouped_don)

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
    result = SelectField("Select won options",choices=[("None","None"),("W","Win"),("L","Loss")])
    filter = SubmitField('Filter')
    type = SelectField("Select type of graph", 
    choices =[("Bar plot","Bar plot"),("Horizontal Bar Plot","Horizontal Bar Plot"),("Box-Whisker","Box-Whisker")],default = "Bar plot")
    x_axis = SelectField("Select Independent Variable",
    choices = [("Donator","Donator"),("Candidate","Candidate"),("Issue","Issue"),("Other","Other"),("State","State")], default = "Candidate")
    facet_result = BooleanField("Facet by won election type")
    color_palette = SelectField("Choose some nifty colors bro",
    choices=[("Blues","Blues"),("Purples","Purples"),("icefire","icefire"),("vlag","vlag")],default = "Icefire")
    run_graph = SubmitField("Create Graph")



    



@bp.route('/correlation',methods=['GET', 'POST'])
def correlation():
    states = Correlation.get_unique_state()
    issues = Correlation.get_unique_issue()
    candidates = Correlation.get_unique_candidate()


    #Candidate = Correlation.get_candidate()
    choice_states = ["None"]
    choice_issues = ["None"]
    choice_candidates = ["None"]
    for s in issues:
        choice_issues.append(s.issue)
    for s in states:
        choice_states.append(s.state_id)
    for s in candidates:      
        choice_candidates.append(s.candidate_id)

    

    # get all correlations
    form = SelectFilters()
    form.state.choices = choice_states
    form.issue.choices = choice_issues
    form.candidate.choices = choice_candidates


    #candidate, issue, result, state
    if form.state.data == "None":
        state = None
    else:
        state = form.state.data

    if form.issue.data == "None":
        issue = None
    else:
        issue = form.issue.data
    
    if form.candidate.data == "None":
        candidate = None
    else:
        candidate = form.candidate.data
    
    if form.result.data == "None":
        result = None
    else:
        result = form.result.data

    if (state is None) & (issue is None) & (candidate is None) & (result is None):
        data = Correlation.get_all()
    else:
        data = Correlation.get_up_to_all(result,state,None,candidate,issue)


    #visualization component
    
    global x
    global y
    global facet
    global color
    facet = False

  
    if form.facet_result.data == True:
            facet = True
    if form.x_axis.data == "Candidate":
            x = [s.candidate_id for s in data]
    elif form.x_axis.data == "Donator":
            x = [s.donator_id for s in data]
    elif form.x_axis.data == "State":
            x = [s.state_id for s in data]
    elif form.x_axis.data == "Issue":
            x = [s.issue for s in data]
    y = [float(s.amount) for s in data]
    color = [s.result for s in data]

    return render_template('correlation.html',
                           data=data,
                           form = form,
                           size_choices_states = len(form.state.choices),
                           size_choices_issues = len(form.state.choices)
            )


            
@bp.route('/visualize')
def visualize():
    fig,ax=plt.subplots(figsize=(6,6))
    ax=sns.set(style="darkgrid")
    plt.xticks(rotation=90)
    if facet:
        sns.barplot(x=x,y=y,estimator="sum",hue=color,palette = "icefire").set(title="Aggregation of Total Donations")
    else:
        sns.barplot(x=x,y=y,estimator="sum",palette = "Blues").set(title="Aggregation of Total Donations")
        
    canvas=FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')

@bp.route('/visualize_states')
def visualize_states(race_data):
    fig,ax=plt.subplots(figsize=(3,3))
    ax=sns.set(style="darkgrid")
    sns.barplot(data = race_data, x=candidate_name, y = total_receipts).set(title = "Total Receipts")    
    canvas=FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')