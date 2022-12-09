from flask import render_template, send_file
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


from .models.issues import Issues
from .models.issues import Industries
from .models.candidates import Candidate_Vote

import textwrap


from flask import Blueprint
bp = Blueprint('issues', __name__)

class SearchIssue(FlaskForm):
    issue_category = StringField('Issue')
    politician = StringField('politician')
    search = SubmitField('Search')

def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_xticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width,
                      break_long_words=break_long_words))
    ax.set_xticklabels(labels, rotation=0)
    

@bp.route('/issues', methods=['GET', 'POST'])
def issues():
    form = SearchIssue()

    all_issues = Issues.get_all()

    donations = Industries.get_all()

    senators = Issues.get_all_senator_names()

    subjects = Issues.get_all_subject_names()

    names = Candidate_Vote.get_all_candidates()

    cid_link = "/candidate/"

    global x
    global total_y
    global individual_y
    global pac_y

    politician_name_formatted = ""

    if form.validate_on_submit():
        all_issues = Issues.get_all_issue(form.issue_category.data)
        all_issues = Issues.get_all_issue_politician(form.issue_category.data, form.politician.data)
        donations = Industries.get_donations_senator(form.politician.data) #has all the donation amounts

        #formatting name for the output
        formatting_name = form.politician.data.split(", ")
        politician_name_formatted = formatting_name[1] + " " + formatting_name[0]

        # print(donations[0].industry[0])
        # print(donations[form.politician.data].industry)

        x = [s.industry[0] for s in donations]
        total_y = [float(s.total_donations[0]) for s in donations]
        individual_y = [float(s.individual_donations[0]) for s in donations]
        pac_y = [float(s.pac_donations) for s in donations]
        print(individual_y)

        candidate_name = form.politician.data
        candidate_name = candidate_name.lower()

        candidate_id = 0
        for name in names:
            if name[0].lower() == candidate_name:
                candidate_id = name[1]
                break
            elif name[0].lower().split(",")[0] == candidate_name.split(",")[0]:
                candidate_id = name[1]
                break
        
        cid_link = "/candidate/" + str(candidate_id)


    return render_template('issues.html', form=form,
                           list_issues=all_issues,
                           list_donations=donations,
                           list_senators=senators,
                           list_subjects=subjects,
                           cid_link=cid_link,
                           politician_name_formatted=politician_name_formatted
                            )

@bp.route('/industry/visualize')
def visualize():
    # print("visualize:", x)
    # print(y)

    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots(1,3)
    fig.set_figheight(20)
    fig.set_figwidth(45)

    ax[0].bar(x,total_y)
    # ax[0].set(title="Total Donations")

    ax[0].set_xticklabels(x, fontsize=20)
    current_values = ax[0].get_yticks()
    ax[0].set_yticklabels(['{:,.0f}'.format(x) for x in current_values], fontsize=20)
    wrap_labels(ax[0], 10)

    ax[0].set_title("Total Donations", fontsize=40)

    ax[1].bar(x,individual_y)
    # ax[1].set(title="Individual Donations")

    ax[1].set_xticklabels(x, fontsize=20)
    current_values = ax[1].get_yticks()
    ax[1].set_yticklabels(['{:,.0f}'.format(x) for x in current_values], fontsize=20)
    wrap_labels(ax[1], 10)

    ax[1].set_title("Individual Donations", fontsize=40)

    ax[2].bar(x,pac_y)
    #ax[2].set(title="PAC Donations")

    ax[2].set_xticklabels(x, fontsize=20)
    current_values = ax[2].get_yticks()
    ax[2].set_yticklabels(['{:,.0f}'.format(x) for x in current_values], fontsize=20)
    wrap_labels(ax[2], 10)

    ax[2].set_title("PAC Donations", fontsize=40)
    # Save it to a temporary buffer.
    img = io.BytesIO()
    fig.savefig(img, bbox_inches="tight")
    img.seek(0)


    # fig,ax=plt.subplots(figsize=(10,10))
    # ax=sns.set(style="darkgrid")
    # sns.barplot(x=x,y=y).set(title="Total Donations by Industry")
    # canvas=FigureCanvas(fig)
    # img = io.BytesIO()
    # fig.savefig(img)
    # img.seek(0)
    return send_file(img,mimetype='img/png')




#     #visualization component
#     global x
#     global y
#     x = [s.issue for s in data]
#     y = [float(s.committee_id) for s in data]
#     return render_template('correlation.html',
#                            data=data,
#                            form = form,
#                            size_choices_states = len(form.state.choices),
#                            size_choices_issues = len(form.state.choices),
#                            optionsForm = optionsForm,
#                            stateTruthy = stateTruthy,
#                            candidateTruthy = candidateTruthy,
#                            passedTruthy = passedTruthy,
#                            issueTruthy = issueTruthy,
#             )


            




