from flask import render_template,flash
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, SelectField,SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from wtforms import BooleanField as WTBool
from .models.committees import Committees

from flask import Blueprint
bp = Blueprint('committees', __name__)

class SearchFirst (FlaskForm):
    query = SelectField('query',choices=['all donations','donations involving','donations to/from'],default='all donations')
    search = SubmitField('Select')
class AllCommittees(FlaskForm):
    from_year = IntegerField('From Year',default=0)
    to_year=IntegerField('To Year',default=2022)
    order_by=SelectField('Order by:',choices=['ID', 'year','donation amount'],default='ID')
    sort=SelectField(choices=['ascending','descending'],default='ascending')
    query = SelectField('query',choices=['all donations', 'donations involving','donations to/from'],default='all donations')
    search = SubmitField('Search')
   # total = SelectMultipleField('Total Sum',choices=['Find total sum'])
    #reset = SubmitField('Reset')
class SearchCommitteeInvolving(FlaskForm):
    from_year = IntegerField('From Year',default=0)
    to_year=IntegerField('To Year',default=2022)
    order_by=SelectField('Order by:',choices=['ID', 'year','donation amount'],default='ID')
    sort=SelectField(choices=['ascending','descending'],default='ascending')
    query = SelectField('query',choices=['all donations', 'donations involving','donations to/from'],default='all donations')
    any_ent = StringField('Entity')
    search = SubmitField('Search')
    #total = SelectMultipleField('Total Sum',choices=[])
class SearchCommitteeToFrom(FlaskForm):
    from_year = IntegerField('From Year',default=0)
    to_year=IntegerField('To Year',default=2022)
    order_by=SelectField('Order by:',choices=['ID', 'year','donation amount'],default='ID')
    sort=SelectField(choices=['ascending','descending'],default='ascending')
    query = SelectField('query',choices=['all donations','donations involving','donations to/from'],default='all donations')
    to_ent = StringField('To entity')
    from_ent = StringField('From entity')
    search = SubmitField('Search')
   # total = SelectMultipleField('Total Sum',choices=[])

@bp.route('/committee', methods=['GET', 'POST'])
def committees():
    output=[]
    form = SearchFirst()
    type_form=''
    searchedcomms=Committees.get_all('ID','ascending')
    if form.validate_on_submit():
        if form.query.data=='donations involving':
            type_form=form.query.data
            form = SearchCommitteeInvolving()
            helper(type_form,form)            
        elif form.query.data=='donations to/from':
            type_form=form.query.data
            form=SearchCommitteeToFrom()
            helper(type_form,form)
        elif form.query.data=='all donations':
            type_form=form.query.data
            form=AllCommittees()
            helper(type_form,form)
            

    #searchedcomms=Committees.get_all_range(form.from_year.data,form.to_year.data,form.order_by.data,form.sort.data)
    if form.validate_on_submit():
        if type_form=='donations involving':
            output.append('You searched for donations involving ' + form.any_ent.data)
            output.append('Date range: '+str(form.from_year.data)+' to ' + str(form.to_year.data))
            #flash('You searched for donations involving ' + form.any_ent.data )
            #flash('Date range: '+str(form.from_year.data)+' to ' + str(form.to_year.data))
            searchedcomms=Committees.get_all_involving(form.any_ent.data, form.from_year.data,form.to_year.data,form.order_by.data,form.sort.data)
        elif type_form=='donations to/from':
            if form.to_ent.data and form.from_ent.data:
                output.append('You searched for donations from ' + form.from_ent.data + ' to ' + form.to_ent.data)
                output.append('Date range: '+str(form.from_year.data)+' to ' + str(form.to_year.data))
                searchedcomms=Committees.get_all_from_to_range(form.to_ent.data, form.from_ent.data, form.from_year.data,form.to_year.data,form.order_by.data,form.sort.data)
            elif form.to_ent.data:
                output.append('You searched for donations to ' + form.to_ent.data)
                output.append('Date range: '+str(form.from_year.data)+' to ' + str(form.to_year.data))
                searchedcomms=Committees.get_all_to_entity_range(form.to_ent.data, form.from_year.data,form.to_year.data,form.order_by.data,form.sort.data)
            elif form.from_ent.data: 
                output.append('You searched for donations from ' + form.from_ent.data)
                output.append('Date range: '+str(form.from_year.data)+' to ' + str(form.to_year.data))
                searchedcomms=Committees.get_all_from_entity_range(form.from_ent.data, form.from_year.data,form.to_year.data,form.order_by.data,form.sort.data)
            else:
                searchedcomms=Committees.get_all_range(form.from_year.data,form.to_year.data,form.order_by.data,form.sort.data)                
        elif type_form=='all donations':
            output.append('Date range: '+str(form.from_year.data)+' to ' + str(form.to_year.data))
            searchedcomms=Committees.get_all_range(form.from_year.data,form.to_year.data,form.order_by.data,form.sort.data)
        output.append('Sorted by: ' + form.order_by.data + ' ' + form.sort.data)
        
    return render_template('committees.html', form=form,type_form=type_form,all_committees=searchedcomms,messages=output)

def helper(query,form):
    return render_template('committees.html',form=form,type_form=query)


    
