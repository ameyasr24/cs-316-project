
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
    total = BooleanField("Calculate Total Sum", default = False)
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

    #the default searchedcomms will just be all of the data with default sort, filter, order parameters
    searchedcomms=Committee.get_all(form1.order_by.data,form1.sort.data,form1.from_date.data,form1.to_date.data, form1.view.data,form1.committee_type.data)
    
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
        tot = form1.total.data
        return redirect(url_for('committees.search',order=o,rows=r,sort=s,query=q,view=v,committee_type=c,from_date=f,to_date=t,total=tot))

    #render the template with form1 data, temp (the rows we would like to display for the current page), and the pagination object
    return render_template('committees.html', form=form1,all_committees=temp,pagination=pagination)

@bp.route('/committee/search', methods=['GET', 'POST'])
def search(): 
    #here we are getting all of the previous request's filtering/viewing parameters
    r = request.args.get('rows', default='25')
    s = request.args.get('sort',default='ascending')
    o = request.args.get('order',default='name')
    q = request.args.get('query',default='')
    v = request.args.get('view',default='All')
    c = request.args.get('committee_type',default='All') 
    f = datetime.strptime(request.args.get('from_date', default='2013-11-01'),'%Y-%m-%d')
    t = datetime.strptime(request.args.get('to_date',default='2022-11-01'),'%Y-%m-%d')
    tot = request.args.get('total')
    output=[]

    #here we are redeclaring form1 with the most recently searched parameters
    form1=SearchFirst(rows=r,sort=s,order_by=o,query=q,view=v,committee_type=c,from_date=f,to_date=t,total=tot)

    #the default searchedcomms will just be all of the data, sorted, filtered, and ordered based on the most recent request's parameters (default is sort='ascending', order_by='name')
    searchedcomms=Committee.get_all(o,s,f,t,v,c)
    err=False
    
    #the following is for getting the searchedcomms if the user has inputted a specific query
    if q:
        searchedcomms=Committee.get_comm(q,o,s,f,t,v,c)
        #if searchedcomms is empty, this means that the query the user specified is not in our database, and we set err to True to return error message when we render the template
        if not searchedcomms:
            err=True
        output.append('You searched for donations involving: '+ q)      

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
        tot = form1.total.data
        return redirect(url_for('committees.search',order=o,rows=r,sort=s,query=q,view=v,messages=output,committee_type=c,from_date=f,to_date=t,total=tot))
    
    if tot and not err:
        total=0
        total = Committee.sumAll(f,t, v,c, q)
        output.append(len(total))
        nontotal = total[1][0]
        total = total[0][0]
#figure out a way to distinguish between if it is 
        if nontotal:
            output.append('Total Donations from ' + q+' : $' +str(total) + 'Total Donations to ' + q+' : $' + str(nontotal))
        elif total:
            output.append('Total Donations from ' + q+' : $' + str(total))
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
        order = form2.order_by.data
        sort = form2.sort.data
        ent = form2.to_ent.data
        search = form2.search.data
        total = form2.total.data
        from_date = form2.from_date.data
        to_date = form2.to_date.data
        recipient = form2.recipient.data
        if ent:
            sentence='You searched for donations involving ' + ent
            if recipient!="All":
                sentence+= " and recipients of type "+ recipient
            output.append(sentence)
        elif not ent:
            if recipient!="All":
                sentence= "You searched for donations involving recipients of type "+ recipient
        searchedcomms=Committee.get_all_range(from_date, to_date,order,sort,cid,recipient,ent)                
        if total:
            sumTotal = Committee.get_sum(from_date, to_date,cid,recipient,ent)
            if sumTotal:
                sumTotal = sumTotal[0]
                if not sumTotal:
                    sumTotal = 0
            else: sumTotal = 0
            output.append('Total Donations: $' +str(sumTotal))
        output.append('Date range: '+str(from_date)+' to ' + str(to_date))
        output.append('Sorted by: ' + order + ' ' + sort)
        
    return render_template('committeepage.html', form=form2,type_form=type_form,all_committees=searchedcomms,messages=output,cname=cname,ctype=ctype)