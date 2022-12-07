
from flask import render_template,flash,redirect,url_for,request,Blueprint
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField,BooleanField, SubmitField, SelectField,SelectMultipleField
from wtforms.validators import ValidationError, DataRequired
from flask_paginate import Pagination
from .models.committees import Committee
bp = Blueprint('committees', __name__)

class SearchFirst (FlaskForm):
    query = StringField('Committee')
    view = SelectField('Election cycle',choices=['All',2016,2018,2020,2022],default="All")
    committee_type=SelectField('Committee type',choices=['All','Party - Qualified','Hybrid PAC - Nonqualified','PAC - Qualified','PAC - Nonqualified','Independent Expenditure-only (Super PACs)','Hybrid PAC - Qualified','Independent Expenditor (person or group)','House','Party - Nonqualified','Communication Cost','Senate','Single-candidate indpendent expenditure','Electioneering Communication'],default="All")
    order_by =SelectField('Order by',choices=['name','date','transaction amount'],default='name')
    sort= SelectField(choices=['ascending','descending'],default='ascending')
    rows=SelectField(choices=['25','50','100','200'],default='25')
    submit = SubmitField('Submit')
class SearchSecond (FlaskForm):
    query = SelectField('query',choices=['all donations','donations involving','donations to candidates'],default='all donations')
    select = SubmitField('Select')
class AllCommittees(FlaskForm):
    from_year = IntegerField('From Year',default=0)
    to_year=IntegerField('To Year',default=2022)
    order_by=SelectField('Order by',choices=['ID', 'year','donation amount'],default='ID')
    sort=SelectField(choices=['ascending','descending'],default='ascending')
    query = SelectField('query',choices=['all donations', 'donations involving'],default='all donations')
    search = SubmitField('Search')
    total = BooleanField("Calculate Total Sum", default = False)
class SearchCommittee(FlaskForm):
    from_year = IntegerField('From Year',default=0)
    to_year=IntegerField('To Year',default=2022)
    order_by=SelectField('Order by',choices=['date','donation amount'],default='date')
    sort=SelectField(choices=['ascending','descending'],default='ascending')
    query = SelectField('query',choices=['all donations', 'donations involving'],default='all donations')
    any_ent = StringField('Entity')
    search = SubmitField('Search')
    total = BooleanField("Calculate Total Sum", default = False)

@bp.route('/committee', methods=['GET', 'POST'])
def committees():
    #get an instance of the form with default data
    form1 = SearchFirst()

    #the default searchedcomms will just be all of the data with the default sort and order (default is sort='ascending', order_by='name')
    searchedcomms=Committee.get_all('name','ascending')
    
    #get current page we are on
    page =request.args.get('page',type=int,default=1)

    #the default viewing is 25 rows/page; get the desired start/stop indices to select tuples to display from the total queried searchedcomms
    rows=25
    i=(page-1)*rows
    temp = searchedcomms[i:i+rows]

    #make new pagination object with current page #, # of all tuples we have queried in searchedcomms, and # rows/page
    pagination =Pagination(page=page,total=len(searchedcomms),per_page=rows)

    #if the user submits the form, make a call to the search function with the inputted filtering.viewing parameters
    if form1.validate_on_submit():
        r = int(form1.rows.data)
        o = form1.order_by.data
        s = form1.sort.data
        q = form1.query.data.upper()
        v = form1.view.data
        c=form1.committee_type.data
        return redirect(url_for('committees.search',order=o,rows=r,sort=s,query=q,view=v,committee_type=c))

    #render the template with form1 data, temp (the rows we would like to display for the current page), and the pagination object
    return render_template('committees.html', form=form1,all_committees=temp,pagination=pagination)

@bp.route('/committee/search', methods=['GET', 'POST'])
def search(): 
    #here we are getting all of the previous request's filtering/viewing parameters
    r = request.args.get('rows')
    s = request.args.get('sort')
    o = request.args.get('order')
    q = request.args.get('query')
    v = request.args.get('view')
    c= request.args.get('committee_type') 

    #here we are redeclaring form1 with the most recently searched parameters
    form1=SearchFirst(rows=r,sort=s,order_by=o,query=q,view=v,committee_type=c)

    #the default searchedcomms will just be all of the data, sorted and ordered based on the most recent request's parameters (default is sort='ascending', order_by='name')
    searchedcomms=Committee.get_all(o,s)
    err=False
    #the following is for getting the searchedcomms if the user has inputted a specific query
    if q:
        searchedcomms=Committee.get_comm(q,o,s)
        #if searchedcomms is empty, this means that the query the user specified is not in our database, and we set err to True to return error message when we render the template
        if not searchedcomms:
            err=True

    #the following is for getting the searchedcomms if the user has not inputted a specific query, but the user has inputted non-default parameters for view and committee_type (default is view='All' and committee_type='All')
    elif not q:
        #make separate sql calls based on whether the user has specified both or either of view and committee_type
        if v=="All" and c!="All":
            searchedcomms = Committee.get_all_type(o,s,c)
        elif v!="All" and c=="All":
            searchedcomms = Committee.get_all_view(o,s,v)
        elif v!="All" and c!="All":
            searchedcomms = Committee.get_all_view_type(o,s,v,c)

    #if the user resubmits the form, make another call to this same function with updated parameters to make another search.
    if form1.validate_on_submit():
        #save each of the following values as parameters to input in the next request
        r = int(form1.rows.data)
        o = form1.order_by.data
        s = form1.sort.data
        q = form1.query.data.upper()
        v = form1.view.data
        c= form1.committee_type.data
        return redirect(url_for('committees.search',order=o,rows=r,sort=s,query=q,view=v,committee_type=c))
    
    #get the current page that we are on in the pagination
    page=request.args.get('page',type=int,default=1)

    #based on the # of rows the user specified they wanted to view per page (r) and the current page we are on, get the desired start/stop indices to select from the total queried searchedcomms
    i=int((page-1)*int(r))
    temp = searchedcomms[i:i+int(r)]

    #make new pagination object with current page #, # of all tuples we have queried in searchedcomms, and # rows/page
    pagination =Pagination(page=page,total=len(searchedcomms),per_page=r)

    #render the template with form1 data, temp (the rows we would like to display for the current page), and the pagination object
    return render_template('committees.html', search=True,form=form1,all_committees=temp,pagination=pagination,err=err)


@bp.route('/committee/<cid>', methods=['GET', 'POST'])
def committee_donations(cid):
    #after routing to the individual committee's page, get 
    cname = Committee.get_name(cid)
    ctype = Committee.get_ctype(cid)
    output=[]
    form1 = SearchSecond()
    form2 = SearchSecond()
    type_form=''
    searchedcomms=Committee.get(cid)
    start = 10
    subtype=0
    if form1.validate_on_submit():
        if form1.query.data=='donations involving':
            type_form=form1.query.data
            form2 = SearchCommitteeInvolving()
            helper(type_form,form1,cname,ctype)            
        elif form1.query.data=='all donations':
            type_form=form1.query.data
            form2=AllCommittees()
            helper(type_form,form1,cname,ctype)  
    
    #searchedcomms=Committees.get_all_range(form.from_year.data,form.to_year.data,form.order_by.data,form.sort.data)
    if form2.validate_on_submit():
        start = -5
        if type_form=='donations involving' :
            if form2.any_ent.data:
                output.append('You searched for donations involving ' + form2.any_ent.data)
                searchedcomms=Committee.get_all_involving(form2.any_ent.data, form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data,cid)
            else:
                searchedcomms=Committee.get_all_range(form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data,cid)                

        elif type_form=='all donations':
            searchedcomms=Committee.get_all_range(form2.from_year.data,form2.to_year.data,form2.order_by.data,form2.sort.data,cid)
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
        
    return render_template('committeepage.html', form=form2,type_form=type_form,all_committees=searchedcomms,start=start,messages=output,cname=cname,ctype=ctype)

def helper(query,form,cname,ctype): 
    start = 10
    return render_template('committeepage.html',form=form,type_form=query,start=start,cname=cname,ctype=ctype)

def helperSum(form,type_form,subtype,cid):
    if type_form=='donations involving':
        return Committee.get_sum_involving(form.any_ent.data,form.from_year.data,form.to_year.data,cid)
    if type_form=='all donations':
        return Committee.get_sum_all(form.from_year.data,form.to_year.data,cid)
        
        
        