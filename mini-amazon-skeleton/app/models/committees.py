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

    #returns all tuples based on matching cid value
    @staticmethod 
    def get(cid): 
        return(app.db.execute(''' 
            SELECT *
            FROM Committee
            WHERE cid = :cid 
            ''',
             cid=cid,
        ))
   
    #returns all data, filtered and ordered on date, sort, order, cycles to view, and committee type parameters
    @staticmethod
    def get_all(order,sort, from_date, to_date,view,type): 
        return (app.db.execute('''
            SELECT *
            FROM Committee c1
            WHERE transaction_date >=:from_date AND transaction_date<=:to_date
                AND (CASE WHEN  :view NOT LIKE 'All' THEN  c1.cycle=:view  ELSE c1.cid!='' END)
                AND (CASE WHEN :type NOT LIKE 'All' THEN  c1.ctype=:type ELSE c1.cid!='' END)
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
            to_date=to_date,
            view=view,
            type=type))

    #returns data involving a particular entity (user can indicate if they want this entity as the donor, recipient, or both data)
    #filtered and ordered on date, sort, order, cycles to view, and committee type parameters
    @staticmethod
    def get_comm(name,order,sort,from_date,to_date,view,type):
        return(app.db.execute('''
            SELECT *
            FROM Committee  
            WHERE (cname=:name OR name_contributor=:name) 
            AND transaction_date >=:from_date AND transaction_date<=:to_date
            AND (CASE WHEN  :view NOT LIKE 'All' THEN  cycle=:view  ELSE cid!='' END)
            AND (CASE WHEN :type NOT LIKE 'All' THEN  ctype=:type ELSE cid!='' END)
            ORDER BY  
                CASE WHEN :sort='ascending' AND :order='name' THEN cname  END ASC,
                CASE WHEN :sort='descending' AND :order='name' THEN cname  END DESC,
                CASE WHEN :sort='ascending' AND :order='date' THEN transaction_date END ASC,
                CASE WHEN :sort='ascending' AND :order='transaction amount' THEN transaction_amount  END ASC,
                CASE WHEN :sort='descending' AND :order='date' THEN transaction_date  END DESC,
                CASE WHEN :sort='descending' AND :order='transaction amount' THEN transaction_amount END DESC 
            ''',
            name=name,
            from_date=from_date,
            to_date=to_date,
            sort=sort,
            order=order,
            view=view,
            type=type))

    #returns data on the committee's individual page given certain search parameters
    @staticmethod
    def get_all_range(from_date, to_date, sort_by,aord,cid,recipient,search_entity): 
        rows = app.db.execute('''
            SELECT *
            FROM Committee
            WHERE  transaction_date >=:y1 AND transaction_date<=:y2 AND cid = :cid
            AND (CASE WHEN :recipient NOT LIKE 'All' THEN  entity_tp=:recipient  ELSE cid!='' END)
            AND (CASE WHEN :search_entity NOT LIKE '' THEN  name_contributor=:search_entity  ELSE cid!='' END)
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
            cid=cid,
            recipient=recipient,
            search_entity=search_entity
            )
        return [Committee (*row) for row in rows]
    
    #returns sum for a committee's individual page given certain search parameters
    @staticmethod
    def get_sum (from_date,to_date,cid, recipient,search_entity):
        rows = app.db.execute('''
            SELECT SUM(transaction_amount)
            FROM Committee
            WHERE transaction_date>=:y1 AND transaction_date<=:y2 AND cid = :cid
                AND (CASE WHEN :recipient NOT LIKE 'All' THEN  entity_tp=:recipient  ELSE cid!='' END)
                AND (CASE WHEN :search_entity NOT LIKE '' THEN  name_contributor=:search_entity  ELSE cid!='' END)
            ''',
                              
            y1=from_date,
            y2=to_date,
            cid=cid,
            recipient=recipient,
            search_entity=search_entity
            )
        return rows[0]
    
    #returns sum of donations that the queried committee distributes (if no queried committee, sum of all tuples given parameters)
    @staticmethod
    def sumTo (from_date,to_date,view, ctype,query):
        rows = app.db.execute('''
            (SELECT SUM(transaction_amount)
            FROM Committee
            WHERE transaction_date>=:y1 AND transaction_date<=:y2 
                AND (CASE WHEN :view NOT LIKE 'All' THEN  cycle=:view  ELSE cid!='' END)
                AND (CASE WHEN :query NOT LIKE '' THEN  cname=:query AND name_contributor!=:query
                 WHEN :query LIKE '' THEN cid!=''
                ELSE cycle='0000' END)
                AND (CASE WHEN :ctype NOT LIKE 'All' THEN  ctype=:ctype  ELSE cid!='' END))
            ''',                
            y1=from_date,
            y2=to_date,
            query=query,
            view=view,
            ctype=ctype
            )
        return rows 
    
    #returns sum of donations that the queried committee receives (if no queried committee, returns nothing)
    @staticmethod
    def sumFrom (from_date,to_date,view, ctype,query):
        rows = app.db.execute('''
            (SELECT SUM (transaction_amount)
            FROM Committee
            WHERE transaction_date>=:y1 AND transaction_date<=:y2 
                AND (CASE WHEN :view NOT LIKE 'All' THEN  cycle=:view  ELSE cid!='' END)
                AND (CASE WHEN :query NOT LIKE '' THEN  name_contributor=:query AND cname!=:query
                ELSE cycle='0000' END)
                AND (CASE WHEN :ctype NOT LIKE 'All' THEN  ctype=:ctype  ELSE cid!='' END))
            ''',                
            y1=from_date,
            y2=to_date,
            query=query,
            view=view,
            ctype=ctype
            )
        return rows 
    
    #returns helpful info to use on committee's individual page
    @staticmethod
    def getInfo(cid):
        rows = app.db.execute('''
            SELECT state_,cname,ctype,candidate_name,candidate_id 
            FROM Committee
            WHERE cid=:cid''',
            cid = cid)
        return rows[0]