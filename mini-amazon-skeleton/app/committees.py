
from flask import render_template,flash,redirect,url_for,request,Blueprint
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.fields import DateField
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
    #total = BooleanField("Calculate Total Sum", default = False)
    from_date = DateField('From Date', format = '%Y-%m-%d', default=datetime.strptime('2013-11-01','%Y-%m-%d'))
    to_date = DateField('To Date', format = '%Y-%m-%d', default=datetime.strptime('2022-11-01','%Y-%m-%d'))
    submit = SubmitField('Submit')
class SearchCommittee(FlaskForm):
    order_by=SelectField('Order by',choices=['date','donation amount'],default='date')
    sort=SelectField(choices=['ascending','descending'],default='ascending')
    to_ent = StringField('Entity')
    search = SubmitField('Search')
    total = BooleanField("Calculate Total Sum", default = False)
    from_date = DateField('From Date', format = '%Y-%m-%d', default=datetime.strptime('2013-11-01','%Y-%m-%d'))
    to_date = DateField('To Date', format = '%Y-%m-%d', default=datetime.strptime('2022-11-01','%Y-%m-%d'))
    recipient=SelectField(choices=['All','Candidate Committee','Organization','Party Organization','Political Action Committee','Committee','Candidate','Individual'],default='All')

@bp.route('/committee', methods=['GET', 'POST'])
def committees():
    #get an instance of the form with default data
    form1 = SearchFirst()

    #the default searchedcomms will just be all of the data with the default sort and order (default is sort='ascending', order_by='name')
    searchedcomms=Committee.get_all(form1.order_by.data,form1.sort.data,form1.from_date.data,form1.to_date.data)
    
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
        c = form1.committee_type.data
        f = form1.from_date.data
        t = form1.to_date.data
        #tot = form1.total.data
        return redirect(url_for('committees.search',order=o,rows=r,sort=s,query=q,view=v,committee_type=c,from_date=f,to_date=t))

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
    c = request.args.get('committee_type') 
    f = datetime.strptime(request.args.get('from_date'),'%Y-%m-%d')
    t = datetime.strptime(request.args.get('to_date'),'%Y-%m-%d')
   #tot = request.args.get('total')
    output=[]

    #here we are redeclaring form1 with the most recently searched parameters
    form1=SearchFirst(rows=r,sort=s,order_by=o,query=q,view=v,committee_type=c,from_date=f,to_date=t)

    #the default searchedcomms will just be all of the data, sorted and ordered based on the most recent request's parameters (default is sort='ascending', order_by='name')
    searchedcomms=Committee.get_all(o,s,f,t)
    err=False
    #the following is for getting the searchedcomms if the user has inputted a specific query
    if q:
        searchedcomms=Committee.get_comm(q,o,s,f,t)
        #if searchedcomms is empty, this means that the query the user specified is not in our database, and we set err to True to return error message when we render the template
        if not searchedcomms:
            err=True
        output.append('You searched for donations involving: '+ q)


    #the following is for getting the searchedcomms if the user has not inputted a specific query, but the user has inputted non-default parameters for view and committee_type (default is view='All' and committee_type='All')
    elif not q:
        #make separate sql calls based on whether the user has specified both or either of view and committee_type
        if v=="All" and c!="All":
            searchedcomms = Committee.get_all_type(o,s,c,f,t)
        elif v!="All" and c=="All":
            searchedcomms = Committee.get_all_view(o,s,v,f,t)
        elif v!="All" and c!="All":
            searchedcomms = Committee.get_all_view_type(o,s,v,c,f,t)
        

    #if the user resubmits the form, make another call to this same function with updated parameters to make another search.
    if form1.validate_on_submit():
        #save each of the following values as parameters to input in the next request
        r = int(form1.rows.data)
        o = form1.order_by.data
        s = form1.sort.data
        q = form1.query.data.upper()
        v = form1.view.data
        c= form1.committee_type.data
        f = form1.from_date.data
        t = form1.to_date.data
        #tot = form1.total.data
        return redirect(url_for('committees.search',order=o,rows=r,sort=s,query=q,view=v,committee_type=c,from_date=f,to_date=t))
    
    #if tot:
     #   total=0
      #  total = Committee.temp(q)
            #total=Committee.sumAllQuery(f,t,v,c,q)
        #elif not q:
         #   total = Committee.sumAll(f,t,v,c)
       # if total!=0:
        #    total = total[0]
        #output.append('Total Donations: $' +str(total))

    #get the current page that we are on in the pagination
    page=request.args.get('page',type=int,default=1)

    #based on the # of rows the user specified they wanted to view per page (r) and the current page we are on, get the desired start/stop indices to select from the total queried searchedcomms
    i=int((page-1)*int(r))
    temp = searchedcomms[i:i+int(r)]

    #make new pagination object with current page #, # of all tuples we have queried in searchedcomms, and # rows/page
    pagination =Pagination(page=page,total=len(searchedcomms),per_page=r)

    #render the template with form1 data, temp (the rows we would like to display for the current page), and the pagination object
    return render_template('committees.html', search=True,form=form1,all_committees=temp,pagination=pagination,err=err,messages=output)


@bp.route('/committee/<cid>', methods=['GET', 'POST'])
def committee_donations(cid):
    #after routing to the individual committee's page, get the committee name, type, and all rows usig that committee's cid
    cname = Committee.get_name(cid)
    ctype = Committee.get_ctype(cid)
    searchedcomms=Committee.get(cid)

    #create an empty array to display messages after searching
    output=[]

    #instantiate a new SearchCommittee() form
    form2 = SearchCommittee()

    type_form='all donations'
    subtype=0
    f=''
    if form2.validate_on_submit():
        if form2.to_ent.data:
            type_form='donations involving'
            sentence='You searched for donations involving ' + form2.to_ent.data 
            if form2.recipient.data=="All":
                searchedcomms=Committee.get_all_involving(form2.to_ent.data, form2.from_date.data,form2.to_date.data,form2.order_by.data,form2.sort.data,cid)
            else:
                sentence+= " and recipients of type "+ form2.recipient.data
                searchedcomms = Committee.get_all_involvingRecipient(form2.to_ent.data, form2.from_date.data,form2.to_date.data,form2.order_by.data,form2.sort.data,cid,form2.recipient.data)
            output.append(sentence)
        elif not form2.to_ent.data:

            if form2.recipient.data=="All":
                searchedcomms=Committee.get_all_range(form2.from_date.data,form2.to_date.data,form2.order_by.data,form2.sort.data,cid)                
            else:
                sentence= "You searched for donations involving recipients of type "+ form2.recipient.data
                searchedcomms = Committee.get_all_Recipient( form2.from_date.data,form2.to_date.data,form2.order_by.data,form2.sort.data,cid,form2.recipient.data)
                output.append(sentence)
        if form2.total.data:
            total = helperSum(form2, type_form,subtype,cid,form2.recipient.data)
            if total:
                total = total[0]
                if not total:
                    total = 0
            else: total = 0
            output.append('Total Donations: $' +str(total))
        output.append('Date range: '+str(form2.from_date.data)+' to ' + str(form2.to_date.data))
        output.append('Sorted by: ' + form2.order_by.data + ' ' + form2.sort.data)
        
    return render_template('committeepage.html', form=form2,type_form=type_form,all_committees=searchedcomms,messages=output,cname=cname,ctype=ctype)


def helperSum(form,type_form,subtype,cid,recipient):
    if type_form=='donations involving' and recipient=="All":
        return Committee.get_sum_involving(form.to_ent.data,form.from_date.data,form.to_date.data,cid)
    if type_form=='donations involving' and recipient!="All":
        return Committee.get_sum_involvingRecipient(form.to_ent.data,form.from_date.data,form.to_date.data,cid,recipient)
    if type_form=='all donations' and recipient=="All":
        return Committee.get_sum_all(form.from_date.data,form.to_date.data,cid)
    if type_form=='all donations' and recipient!="All":
        return Committee.get_sum_allRecipient(form.from_date.data,form.to_date.data,cid,recipient)
        
        
        