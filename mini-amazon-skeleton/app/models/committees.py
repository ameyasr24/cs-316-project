from flask import current_app as app


class Committee:
    def __init__(self,tid,cid ,rpt , transaction_tp,entity_tp, name_contributor ,
    state_ ,
    transaction_date,
    transaction_amount ,
    other_id ,
    did,
    year,
    cycle,cname,candidate_id):
        self.tid=tid
        self.cid =cid
        self.rpt = rpt 
        self.transaction_tp=transaction_tp
        self.entity_tp   =entity_tp
        self.name_contributor=name_contributor
        self.state_=state_
        self.transaction_date=transaction_date
        self.transaction_amount =transaction_amount
        self.other_id =other_id
        self.did  =did
        self.year=year
        self.cycle=cycle
        self.cname=cname
        self.candidate_id=candidate_id

    @staticmethod 
    def get(cid): #gets everything by cid value
        rows = app.db.execute('''
SELECT cname
FROM Committee
WHERE cid = :cid
''',
                              cid=cid)
        return Committee(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(order,sort): #just gets everyting in the table
        return (app.db.execute('''
SELECT *
FROM Committee c1
ORDER BY  
        CASE WHEN :sort='ascending' AND :order='name' THEN c1.cname  END ASC,
        CASE WHEN :sort='descending' AND :order='name' THEN c1.cname  END DESC,
        CASE WHEN :sort='ascending' AND :order='election cycle' THEN c1.cycle END ASC,
        CASE WHEN :sort='ascending' AND :order='total receipts' THEN c1.transaction_amount  END ASC,
        CASE WHEN :sort='descending' AND :order='election cycle' THEN c1.cycle  END DESC,
        CASE WHEN :sort='descending' AND :order='total receipts' THEN c1.transaction_amount END DESC  
    
        
''',
                              sort=sort,
                              order=order))


    @staticmethod
    def get_comm(name,order,sort):
        return(app.db.execute('''
SELECT *
FROM Committee  WHERE cname=:name
ORDER BY  
        CASE WHEN :sort='ascending' AND :order='name' THEN cname  END ASC,
        CASE WHEN :sort='descending' AND :order='name' THEN cname  END DESC,
        CASE WHEN :sort='ascending' AND :order='election cycle' THEN cycle END ASC,
        CASE WHEN :sort='ascending' AND :order='total receipts' THEN total_receipts  END ASC,
        CASE WHEN :sort='descending' AND :order='election cycle' THEN cycle  END DESC,
        CASE WHEN :sort='descending' AND :order='total receipts' THEN total_receipts END DESC 
    
        
''',
                              name=name,
                              sort=sort,
                              order=order))
    @staticmethod
    def get_name(cid):
        rows = app.db.execute('''
SELECT cname
FROM Committee  WHERE cid=:cid
        
''',
                              
                              cid=cid)
        return rows[0]