from flask import current_app as app


class Committee:
    def __init__(self,tid,cid ,rpt , transaction_tp,entity_tp, name_contributor ,
    state_ ,
    transaction_date,
    transaction_amount ,
    other_id ,
    did,
    year,
    cycle,cname,ctype,candidate_id,candidate_name):
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
        self.cname=cname,
        self.ctype=ctype,
        self.candidate_id=candidate_id
        self.candidate_name=candidate_name


    @staticmethod 
    def get(cid): #gets everything by cid value
        return(app.db.execute('''
SELECT *
FROM Committee
WHERE cid = :cid
    
''',
                              cid=cid,
                             ))

    @staticmethod
    def get_all(order,sort, from_date, to_date): #just gets everyting in the table
        return (app.db.execute('''
SELECT *
FROM Committee c1
WHERE transaction_date >=:from_date AND transaction_date<=:to_date
ORDER BY  
        CASE WHEN :sort='ascending' AND :order='name' THEN c1.cname  END ASC,
        CASE WHEN :sort='descending' AND :order='name' THEN c1.cname  END DESC,
        CASE WHEN :sort='ascending' AND :order='date' THEN c1.transaction_date END ASC,
        CASE WHEN :sort='ascending' AND :order='transaction amount' THEN c1.transaction_amount  END ASC,
        CASE WHEN :sort='descending' AND :order='date' THEN c1.transaction_date  END DESC,
        CASE WHEN :sort='descending' AND :order='transaction amount' THEN c1.transaction_amount END DESC  
    
        
''',
                              sort=sort,
                              order=order,
                              from_date=from_date,
                              to_date=to_date))
    def get_all_view(order,sort,view,from_date,to_date): #just gets everyting in the table
        return (app.db.execute('''
SELECT *
FROM Committee c1
WHERE c1.cycle=:view AND transaction_date >=:from_date AND transaction_date<=:to_date
ORDER BY  
        CASE WHEN :sort='ascending' AND :order='name' THEN c1.cname  END ASC,
        CASE WHEN :sort='descending' AND :order='name' THEN c1.cname  END DESC,
        CASE WHEN :sort='ascending' AND :order='date' THEN c1.transaction_date END ASC,
        CASE WHEN :sort='ascending' AND :order='transaction amount' THEN c1.transaction_amount  END ASC,
        CASE WHEN :sort='descending' AND :order='date' THEN c1.transaction_date  END DESC,
        CASE WHEN :sort='descending' AND :order='transaction amount' THEN c1.transaction_amount END DESC  
    
        
''',
                              sort=sort,
                              view=view,
                              order=order,
                              from_date=from_date,
                              to_date=to_date))
    def get_all_type(order,sort,type,from_date,to_date): #just gets everyting in the table
        return (app.db.execute('''
SELECT *
FROM Committee c1
WHERE c1.ctype=:type AND transaction_date >=:from_date AND transaction_date<=:to_date
ORDER BY  
        CASE WHEN :sort='ascending' AND :order='name' THEN c1.cname  END ASC,
        CASE WHEN :sort='descending' AND :order='name' THEN c1.cname  END DESC,
        CASE WHEN :sort='ascending' AND :order='date' THEN c1.transaction_date END ASC,
        CASE WHEN :sort='ascending' AND :order='transaction amount' THEN c1.transaction_amount  END ASC,
        CASE WHEN :sort='descending' AND :order='date' THEN c1.transaction_date  END DESC,
        CASE WHEN :sort='descending' AND :order='transaction amount' THEN c1.transaction_amount END DESC  
''',
                              sort=sort,
                              type=type,
                              order=order,
                              from_date=from_date,
                              to_date=to_date))

    def get_all_view_type(order,sort,view,type,from_date,to_date): #just gets everyting in the table
        return (app.db.execute('''
SELECT *
FROM Committee c1
WHERE c1.cycle=:view AND c1.ctype=:type AND transaction_date >=:from_date AND transaction_date<=:to_date
ORDER BY  
        CASE WHEN :sort='ascending' AND :order='name' THEN c1.cname  END ASC,
        CASE WHEN :sort='descending' AND :order='name' THEN c1.cname  END DESC,
        CASE WHEN :sort='ascending' AND :order='date' THEN c1.transaction_date END ASC,
        CASE WHEN :sort='ascending' AND :order='transaction amount' THEN c1.transaction_amount  END ASC,
        CASE WHEN :sort='descending' AND :order='date' THEN c1.transaction_date  END DESC,
        CASE WHEN :sort='descending' AND :order='transaction amount' THEN c1.transaction_amount END DESC  
    
        
''',
                              sort=sort,
                              view=view,
                              type=type,
                              order=order,
                              from_date=from_date,
                              to_date=to_date))

    @staticmethod
    def get_comm(name,order,sort,from_date,to_date):
        return(app.db.execute('''
SELECT *
FROM Committee  WHERE (cname=:name OR name_contributor=:name) AND transaction_date >=:from_date AND transaction_date<=:to_date
ORDER BY  
        CASE WHEN :sort='ascending' AND :order='name' THEN cname  END ASC,
        CASE WHEN :sort='descending' AND :order='name' THEN cname  END DESC,
        CASE WHEN :sort='ascending' AND :order='election cycle' THEN cycle END ASC,
        CASE WHEN :sort='ascending' AND :order='transaction amount' THEN transaction_amount  END ASC,
        CASE WHEN :sort='descending' AND :order='election cycle' THEN cycle  END DESC,
        CASE WHEN :sort='descending' AND :order='transaction amount' THEN transaction_amount END DESC 
    
        
''',
                              name=name,
                              from_date=from_date,
                              to_date=to_date,
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
    @staticmethod
    def get_ctype(cid):
        rows = app.db.execute('''
SELECT ctype
FROM Committee  WHERE cid=:cid
        
''',
                              
                              cid=cid)
        return rows[0]


    

    @staticmethod
    def get_all_range(from_date, to_date, sort_by,aord,cid): #gets everything in the table given a range of dates
        rows = app.db.execute('''
            SELECT *
            FROM Committee
            WHERE  transaction_date >=:y1 AND transaction_date<=:y2 AND cid = :cid
            ORDER BY 
        CASE WHEN :AD='ascending' AND :s='date' THEN transaction_date END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN transaction_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN transaction_amount END DESC,
        CASE WHEN :AD='descending' AND :s='date' THEN transaction_date END DESC
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              cid=cid
                              )
        return [Committee (*row) for row in rows]

    @staticmethod
    def get_all_Recipient(from_date, to_date, sort_by,aord,cid,recipient): #gets everything in the table given a range of dates
        rows = app.db.execute('''
            SELECT *
            FROM Committee
            WHERE  transaction_date >=:y1 AND transaction_date<=:y2 AND cid = :cid AND entity_tp=:recipient
            ORDER BY 
        CASE WHEN :AD='ascending' AND :s='date' THEN transaction_date END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN transaction_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN transaction_amount END DESC,
        CASE WHEN :AD='descending' AND :s='date' THEN transaction_date END DESC
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              recipient=recipient,
                              AD=aord,
                              cid=cid
                              )
        return [Committee (*row) for row in rows]

    
    @staticmethod
    def get_all_involving(search_entity,from_date,to_date, sort_by,aord,cid):
        rows = app.db.execute('''
            SELECT *        FROM Committee
            WHERE cid = :cid AND ( name_contributor=:entity) AND transaction_date>=:y1 AND transaction_date<=:y2
           ORDER BY 
        CASE WHEN :AD='ascending' AND :s='date' THEN transaction_date END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN transaction_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN transaction_amount END DESC,
        CASE WHEN :AD='descending' AND :s='date' THEN transaction_date END DESC
            ''',
                              entity=search_entity,
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              cid=cid
                              )
        return [Committee(*row) for row in rows]
    @staticmethod
    def get_all_involvingRecipient(search_entity,from_date,to_date, sort_by,aord,cid,recipient):
        rows = app.db.execute('''
            SELECT *        FROM Committee
            WHERE cid = :cid AND ( name_contributor=:entity) AND transaction_date>=:y1 AND transaction_date<=:y2 AND entity_tp=:recipient
           ORDER BY 
        CASE WHEN :AD='ascending' AND :s='date' THEN transaction_date END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN transaction_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN transaction_amount END DESC,
        CASE WHEN :AD='descending' AND :s='date' THEN transaction_date END DESC
            ''',
                              entity=search_entity,
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              cid=cid,
                              recipient=recipient
                              )
        return [Committee(*row) for row in rows]

    @staticmethod
    def get_sum_all (from_date,to_date,cid):
        rows = app.db.execute('''
            SELECT SUM(transaction_amount)
            FROM Committee
            WHERE transaction_date>=:y1 AND transaction_date<=:y2 AND cid = :cid
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              cid=cid
                              )
        return rows[0]
    @staticmethod
    def get_sum_involving (any_ent, from_date,to_date,cid):
        rows = app.db.execute('''
            SELECT SUM(transaction_amount)
            FROM Committee
            WHERE transaction_date>=:y1 AND transaction_date<=:y2 AND cid = :cid AND (name_contributor=:entity) 
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              entity=any_ent,
                              cid=cid
                              )
        return rows[0]
    @staticmethod
    def get_sum_allRecipient (from_date,to_date,cid,recipient):
        rows = app.db.execute('''
            SELECT SUM(transaction_amount)
            FROM Committee
            WHERE transaction_date>=:y1 AND transaction_date<=:y2 AND cid = :cid AND entity_tp=:recipient
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              recipient=recipient,
                              cid=cid
                              )
        return rows[0]
    @staticmethod
    def get_sum_involvingRecipient (any_ent, from_date,to_date,cid,recipient):
        rows = app.db.execute('''
            SELECT SUM(transaction_amount)
            FROM Committee
            WHERE transaction_date>=:y1 AND transaction_date<=:y2 AND cid = :cid AND (name_contributor=:entity) AND cid = :cid AND entity_tp=:recipient 
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              entity=any_ent,
                              recipient=recipient,
                              cid=cid
                              )
        return rows[0]
    
