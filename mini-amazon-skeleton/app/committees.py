from flask import render_template,flash
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField,BooleanField, SubmitField, SelectField,SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_paginate import Pagination, get_page_parameter
from flask import request

from wtforms import BooleanField as WTBool
from .models.committee_donations import Committee_Donations
from .models.committees import Committee
from flask import Blueprint
bp = Blueprint('committees', __name__)

class SearchFirst (FlaskForm):
    query = StringField('Committee')
    order_by =SelectField('Order by',choices=['name','election cycle','total receipts'],default='name')
    sort= SelectField(choices=['ascending','descending'],default='ascending')
    rows=SelectField(choices=['25','50','100','200'],default='25')
    submit = SubmitField('Submit')
class SearchSecond (FlaskForm):
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
    rows=25
    form1 = SearchFirst()
    searchedcomms=Committee.get_all('name','ascending')
    page =request.args.get('page',type=int,default=1)
    search = False
    q = request.args.get('q')
    if q:
        search = True
    try:
        page=int(request.args.get('page',1))
    
    except ValueError:
        page = 1
    i=(page-1)*rows
    temp = searchedcomms[i:i+rows]
    pagination =Pagination(page=page,total=len(searchedcomms),per_page=rows)

    if form1.validate_on_submit():
        rows = int(form1.rows.data)
        order = form1.order_by.data
        sort = form1.sort.data
        query = form1.query.data.upper()
        if query:
            searchedcomms=Committee.get_comm(query,order,sort)
            if not searchedcomms:
                return render_template('committees.html',form=form1, allcommittees=searchedcomms, err=True,pagination=pagination)
        elif not query:
            searchedcomms=Committee.get_all(order,sort)
        page =request.args.get('page',type=int,default=1)
        search = False
        q = request.args.get('q')
        if q:
            search = True
        try:
            page=int(request.args.get('page',1))
        
        except ValueError:
            page = 1
        i=int((page-1)*rows)
        temp = searchedcomms[i:i+rows]
        pagination =Pagination(page=page,total=len(searchedcomms),per_page=rows)
        return render_template('committees.html', form=form1,all_committees=temp,ival=i,pagination=pagination)

    return render_template('committees.html', form=form1,all_committees=temp,pagination=pagination)

@bp.route('/committee/<cid>', methods=['GET', 'POST'])
def committee_donations(cid):
    comm = Committee.get_name(cid)
    output=[]
    form1 = SearchSecond()
    form2 = SearchSecond()
    type_form=''
    searchedcomms=Committee_Donations.get(cid,'ID','ascending')
    start = 10
    subtype=0
    if form1.validate_on_submit():
        if form1.query.data=='donations involving':
            type_form=form1.query.data
            form2 = SearchCommitteeInvolving()
            helper(type_form,form1,comm)            
        elif form1.query.data=='donations to/from':
            type_form=form1.query.data
            form2=SearchCommitteeToFrom()
            helper(type_form,form1,comm)
        elif form1.query.data=='all donations':
            type_form=form1.query.data
            form2=AllCommittees()
            helper(type_form,form1,comm)  
    
    #searchedcomms=Committees.get_all_range(form.from_year.data,form.to_year.data,form.order_by.data,form.sort.data)
    if form2.validate_on_submit():
        start = -5
        if type_form=='donations involving' :
            if form2.any_ent.data:
                output.append('You searched for donations involving ' + form2.any_ent.data)
                searchedcomms=Committee_Donations.get_all_involving(form2.any_ent.data, form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data,cid)
            else:
                searchedcomms=Committee_Donations.get_all_range(form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data,cid)                

        elif type_form=='donations to/from':
            if form2.to_ent.data and form2.from_ent.data:
                subtype=1
                output.append('You searched for donations from ' + form2.from_ent.data + ' to ' + form2.to_ent.data)
                searchedcomms=Committee_Donations.get_all_from_to_range(form2.to_ent.data, form2.from_ent.data, form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data,cid)
            elif form2.to_ent.data:
                subtype=2
                output.append('You searched for donations to ' + form2.to_ent.data)
                searchedcomms=Committee_Donations.get_all_to_entity_range(form2.to_ent.data, form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data,cid)
            elif form2.from_ent.data: 
                subtype=3
                output.append('You searched for donations from ' + form2.from_ent.data)
                searchedcomms=Committee_Donations.get_all_from_entity_range(form2.from_ent.data, form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data,cid)
            else:
                searchedcomms=Committee_Donations.get_all_range(form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data,cid)                
        elif type_form=='all donations':
            searchedcomms=Committee_Donations.get_all_range(form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data,cid)
        if form2.total.data:
            total = helperSum(form2, type_form,subtype,cid)
            if total:
                total = total[0]
                if not total:
                    total = 0
            else: total = 0
            output.append('Total Donations: $' +str(total))
        output.append('Date range: '+str(form2.from_year.data)+' to ' + str(form2.to_year.data))
        output.append('Sorted by: ' + form2.order_by.data + ' ' + form2.sort.data)
        
    return render_template('committeepage.html', form=form2,type_form=type_form,all_committees=searchedcomms,start=start,messages=output,comm=comm)

def helper(query,form,comm): 
    start = 10
    return render_template('committeepage.html',form=form,type_form=query,start=start,comm=comm)

def helperSum(form,type_form,subtype,cid):
    if type_form=='donations involving':
        return Committee_Donations.get_sum_involving(form.any_ent.data,form.from_year.data,form.to_year.data,cid)
    if type_form=='donations to/from':
        if subtype==1:
            return Committee_Donations.get_sum_from_to(form.from_ent.data,form.to_ent.data,form.from_year.data,form.to_year.data,cid)
        elif subtype==2:
            return Committee_Donations.get_sum_to(form.to_ent.data,form.from_year.data,form.to_year.data,cid)
        elif subtype==3:
            return Committee_Donations.get_sum_from(form.from_ent.data,form.from_year.data,form.to_year.data,cid)
    if type_form=='all donations':
        return Committee_Donations.get_sum_all(form.from_year.data,form.to_year.data,cid)