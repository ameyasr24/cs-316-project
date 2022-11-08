from flask import render_template,flash
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.committees import Committees

from flask import Blueprint
bp = Blueprint('committees', __name__)


class SearchCommittee(FlaskForm):
    to_ent = StringField('To entity')
    from_ent = StringField('From entity')
    #eventually change to_ent to make everything lowercase
    from_year = IntegerField('From Year',default=0)
    to_year=IntegerField('To Year',default=2022)
   # order_by=SelectField('Order by:',choices=['cid', 'date ascending','date descending'],default='cid')
    search = SubmitField('Search')

# original committee without the form function in the html file
# @bp.route('/committee', methods=['GET', 'POST'])
# def committees():
#     comms = Committees.get_all()
#     return render_template('committees.html', 
#                            all_committees=comms)


@bp.route('/committee', methods=['GET', 'POST'])
def committees():
    #to do: if there is no to entity provided, get all from from_entity from given times/default
    # if there is not from entity provided, get all from to_entity from given times/default
    #if both, then get all entities from given times/default
    
    form = SearchCommittee()
    searchedcomms=Committees.get_all()
    if form.validate_on_submit():
        if form.to_ent.data or form.from_ent.data:
            if form.to_ent.data and form.from_ent.data:
                flash('You searched for donations from ' + form.from_ent.data + ' to ' + form.to_ent.data)
                flash('Date range: '+str(form.from_year.data)+' to ' + str(form.to_year.data))
                searchedcomms=Committees.get_all_from_to_range(form.to_ent.data, form.from_ent.data, form.from_year.data,form.to_year.data)
            elif form.to_ent.data:
                flash('You searched for donations to ' + form.to_ent.data)
                flash('Date range: '+str(form.from_year.data)+' to ' + str(form.to_year.data))
                searchedcomms=Committees.get_all_to_entity_range(form.to_ent.data, form.from_year.data,form.to_year.data)
            elif form.from_ent.data: 
                flash('You searched for donations from ' + form.from_ent.data)
                flash('Date range: '+str(form.from_year.data)+' to ' + str(form.to_year.data))
                searchedcomms=Committees.get_all_from_entity_range(form.from_ent.data, form.from_year.data,form.to_year.data)
        else:
            flash('Date range: '+str(form.from_year.data)+' to ' + str(form.to_year.data))
            searchedcomms=Committees.get_all_range(form.from_year.data,form.to_year.data)
    #    flash('Sorted by:' + form.order_by.data)
     #   if form.order_by.data=='date ascending':
      #      searchedcomms=Committees.sort_by_date_asc(searchedcomms)
      #  elif form.order_by.data=='date descending':
       #     searchedcomms=Committees.sort_by_date_desc(searchedcomms)
    return render_template('committees.html', form=form,all_committees=searchedcomms)



    
