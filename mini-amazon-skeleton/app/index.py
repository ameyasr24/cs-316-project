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

#Form to set graph and table paremeters
class SelectOptions(FlaskForm):
    #Option to hold state options
    state = SelectField("Select a state: ")
    #Option to hold issue options
    issue = SelectField("Select an issue: ")
    #Option to hold candidate options
    candidate = SelectField("Select a candidate: ")
    #Option to filter by result (winning candidate)
    result = SelectField("Select won options: ",choices=[("None","None"),("W","Win"),("L","Loss")])
    #Button to filter
    filter = SubmitField('Filter')
    #Option to select the type of graph user would like
    type_graph = SelectField("Select type of graph: ", 
    choices =[("Bar plot","Bar plot"),("Dotplot","Dotplot"),("Box-Whisker","Box-Whisker"),("Violin","Violin")],default = "Bar plot")
    #Option to hold state options
    x_axis = SelectField("Select Independent Variable: ",
    choices = [("Donator","Donator"),("Candidate","Candidate"),("Issue","Issue"),("State","State")], default = "Issue")
    #Option to facet by result (if applicable)
    facet_result = SelectField("Facet by election result?",choices=[(True,"Yes"),(False,"No")],default = "No")
    #option to choose color pallette
    color_palette = SelectField("Choose your pallete: ",
    choices=[("Blues","Blues"),("Purples","Purples"),("icefire","icefire"),("vlag","vlag")],default = "icefire")
    #option to run the graph
    run_graph = SubmitField("Create Graph")
    #option to set a mininum threshold on donations
    amount_threshold = SelectField("Choose amount threshold",choices = [("None","None"),(5000,5000),(10000,10000),(50000,50000),(100000,1000000)],default = "None")



    



@bp.route('/correlation',methods=['GET', 'POST'])
def correlation():
    #get unique state options
    states = Correlation.get_unique_state()
    #get unique issue options
    issues = Correlation.get_unique_issue()
    #get unique candidate options
    candidates = Correlation.get_unique_candidate()


    #list to hold state options
    choice_states = ["None"]
    #list to hold issue options
    choice_issues = ["None"]
    #list to hold candidate options
    choice_candidates = ["None"]
    #loops to fill out the lists above
    for s in issues:
        choice_issues.append(s.issue)
    for s in states:
        choice_states.append(s.state_id)
    for s in candidates:      
        choice_candidates.append(s.candidate_id)

    

    
    #add form to view
    form = SelectOptions()

    #Get unique options for state, issues, candidates
    form.state.choices = choice_states
    form.issue.choices = choice_issues
    form.candidate.choices = choice_candidates


    #set state data based on selected option
    if form.state.data == "None":
        state = None
    else:
        state = form.state.data
    #set issue data based on selected option
    if form.issue.data == "None":
        issue = None
    else:
        issue = form.issue.data
    #set state data based on selected option
    if form.candidate.data == "None":
        candidate = None
    else:
        candidate = form.candidate.data
    #set result option based on selection
    if form.result.data == "None":
        result = None
    else:
        result = form.result.data
    #set threshold option based on selection
    if form.amount_threshold.data == "None":
        amount = None
    else:
        amount = form.amount_threshold.data
    #run queries to get type of data
    if (state is None) & (issue is None) & (candidate is None) & (result is None):
        data = Correlation.get_all()
    else:
        data = Correlation.get_up_to_all(result,state,None,candidate,issue,amount)


    #visualization component
    
    #global x option for viz
    global x
    #global y option for viz
    global y
    #global facet option for viz
    global facet
    #global color option for viz
    global color
    #global hue option for viz
    global hues
    #global type of graph option for viz
    global type_of
    #initialize facet
    facet = False
    #initialize x_label
    global x_label
    #set hue options based on form entry
    hues = form.color_palette.data
    #set graph options based on form entry
    type_of = form.type_graph.data
    #set x_label options based on form entry
    x_label = form.x_axis.data
    
    ###ALL IF STATEMENTS CHOOSE INDEPENDENT VARIABLE
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
    #Get amount variables
    y = [float(s.amount) for s in data]
    #set color/facet variable
    color = [s.result for s in data]
    #return to template
    return render_template('correlation.html',
                           data=data,
                           form = form,
                           size_choices_states = len(form.state.choices),
                           size_choices_issues = len(form.state.choices)
            )


#Visualization function        
@bp.route('/visualize')
def visualize():
    #initialize plot
    fig,ax=plt.subplots(figsize=(20,20))
    #Setup visual options for the plot
    ax=sns.set_style("dark")
    ax=sns.set(rc={'figure.figsize':(11.7,8.27)})
    ax=sns.set(style="darkgrid")
    plt.xticks(rotation=45)
    plt.style.use('fivethirtyeight')
    plt.xlabel(x_label)
    plt.ylabel("Amount donated")
    title_graph = "Aggregation of Total Donations with " + x_label

    #SETUP PLOT BASED ON PASSED TYPE OF GRAPH AND FACET
    if type_of == "Bar plot":
        if facet:
            sns.barplot(x=x,y=y,estimator="sum",hue=color,palette = hues,errorbar=None).set(title=title_graph)
        else:
            sns.barplot(x=x,y=y,estimator="sum",palette = hues,errorbar=None).set(title=title_graph)
    elif type_of == "Violin":
        if facet:
            sns.violinplot(x=x,y=y,estimator="sum",hue=color,palette = hues,errorbar=None).set(title=title_graph)
        else:
            sns.violinplot(x=x,y=y,estimator="sum",palette = hues,errorbar=None).set(title=title_graph)
    elif type_of == "Box-whisker":
        if facet:
            sns.boxplot(x=x,y=y,estimator="sum",hue=color,palette = hues).set(title=title_graph)
        else:
            sns.boxplot(x=x,y=y,estimator="sum",palette = hues).set(title=title_graph)
    elif type_of == "Dotplot":
        if facet:
            sns.scatterplot(x=x,y=y,hue=color,palette = hues,errorbar=None).set(title=title_graph)
        else:
            sns.scatterplot(x=x,y=y,palette = hues,errorbar=None).set(title=title_graph)
    #GET CANVAS
    canvas=FigureCanvas(fig)
    #PASS TO BYTES/BUFFER TO SEND TO HTML 
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