from flask import render_template,flash
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, SelectField,SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from wtforms import BooleanField as WTBool
from .models.committee_donations import Committee_Donations
from .models.committee import Committee
from flask import Blueprint
bp = Blueprint('committee_donations', __name__)

class SearchFirst (FlaskForm):
    query = SelectField('query',choices=['all donations','donations involving','donations to/from'],default='all donations')
    select = SubmitField('Select')
class AllCommittees(FlaskForm):
    from_year = IntegerField('From Year',default=0)
    to_year=IntegerField('To Year',default=2022)
    order_by=SelectField('Order by',choices=['ID', 'year','donation amount'],default='ID')
    sort=SelectField(choices=['ascending','descending'],default='ascending')
    query = SelectField('query',choices=['all donations', 'donations involving','donations to/from'],default='all donations')
    search = SubmitField('Search')
    total = BooleanField("Calculate Total Sum", default = False)
class SearchCommitteeInvolving(FlaskForm):
    from_year = IntegerField('From Year',default=0)
    to_year=IntegerField('To Year',default=2022)
    order_by=SelectField('Order by',choices=['ID', 'year','donation amount'],default='ID')
    sort=SelectField(choices=['ascending','descending'],default='ascending')
    query = SelectField('query',choices=['all donations', 'donations involving','donations to/from'],default='all donations')
    any_ent = StringField('Entity')
    search = SubmitField('Search')
    total = BooleanField("Calculate Total Sum", default = False)
class SearchCommitteeToFrom(FlaskForm):
    from_year = IntegerField('From Year',default=0)
    to_year=IntegerField('To Year',default=2022)
    order_by=SelectField('Order by',choices=['ID', 'year','donation amount'],default='ID')
    sort=SelectField(choices=['ascending','descending'],default='ascending')
    query = SelectField('query',choices=['all donations','donations involving','donations to/from'],default='all donations')
    to_ent = StringField('To entity')
    from_ent = StringField('From entity')
    search = SubmitField('Search')
    total = BooleanField("Calculate Total Sum", default = False)

@bp.route('/committee', methods=['GET', 'POST'])
def committees():
    output=[]
    form1 = SearchFirst()
    form2 = SearchFirst()
    type_form=''
    searchedcomms=Committees.get_all('ID','ascending')
    start = 10
    subtype=0
    if form1.validate_on_submit():
        if form1.query.data=='donations involving':
            type_form=form1.query.data
            form2 = SearchCommitteeInvolving()
            helper(type_form,form1)            
        elif form1.query.data=='donations to/from':
            type_form=form1.query.data
            form2=SearchCommitteeToFrom()
            helper(type_form,form1)
        elif form1.query.data=='all donations':
            type_form=form1.query.data
            form2=AllCommittees()
            helper(type_form,form1)
            

    #searchedcomms=Committees.get_all_range(form.from_year.data,form.to_year.data,form.order_by.data,form.sort.data)
    if form2.validate_on_submit():
        start = -5
        if type_form=='donations involving' :
            if form2.any_ent.data:
                output.append('You searched for donations involving ' + form2.any_ent.data)
                searchedcomms=Committees.get_all_involving(form2.any_ent.data, form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data)
            else:
                searchedcomms=Committees.get_all_range(form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data)                

        elif type_form=='donations to/from':
            if form2.to_ent.data and form2.from_ent.data:
                subtype=1
                output.append('You searched for donations from ' + form2.from_ent.data + ' to ' + form2.to_ent.data)
                searchedcomms=Committees.get_all_from_to_range(form2.to_ent.data, form2.from_ent.data, form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data)
            elif form2.to_ent.data:
                subtype=2
                output.append('You searched for donations to ' + form2.to_ent.data)
                searchedcomms=Committees.get_all_to_entity_range(form2.to_ent.data, form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data)
            elif form2.from_ent.data: 
                subtype=3
                output.append('You searched for donations from ' + form2.from_ent.data)
                searchedcomms=Committees.get_all_from_entity_range(form2.from_ent.data, form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data)
            else:
                searchedcomms=Committees.get_all_range(form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data)                
        elif type_form=='all donations':
            searchedcomms=Committees.get_all_range(form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data)
        if form2.total.data:
            total = helperSum(form2, type_form,subtype)
            output.append('Total Donations: $' +str(total[0]))
        output.append('Date range: '+str(form2.from_year.data)+' to ' + str(form2.to_year.data))
        output.append('Sorted by: ' + form2.order_by.data + ' ' + form2.sort.data)
        
    return render_template('committees.html', form=form2,type_form=type_form,all_committees=searchedcomms,start=start,messages=output)

def helper(query,form):
    start = 10
    return render_template('committees.html',form=form,type_form=query,start=start)

def helperSum(form,type_form,subtype):
    if type_form=='donations involving':
        return Committees.get_sum_involving(form.any_ent.data,form.from_year.data,form.to_year.data)
    if type_form=='donations to/from':
        if subtype==1:
            return Committees.get_sum_from_to(form.from_ent.data,form.to_ent.data,form.from_year.data,form.to_year.data)
        elif subtype==2:
            return Committees.get_sum_to(form.to_ent.data,form.from_year.data,form.to_year.data)
        elif subtype==3:
            return Committees.get_sum_from(form.from_ent.data,form.from_year.data,form.to_year.data)
    if type_form=='all donations':
        return Committees.get_sum_all(form.from_year.data,form.to_year.data)