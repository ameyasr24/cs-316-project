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
    def get_all(order,sort): #just gets everyting in the table
        return (app.db.execute('''
SELECT *
FROM Committee c1
ORDER BY  
        CASE WHEN :sort='ascending' AND :order='name' THEN c1.cname  END ASC,
        CASE WHEN :sort='descending' AND :order='name' THEN c1.cname  END DESC,
        CASE WHEN :sort='ascending' AND :order='date' THEN c1.transaction_date END ASC,
        CASE WHEN :sort='ascending' AND :order='transaction amount' THEN c1.transaction_amount  END ASC,
        CASE WHEN :sort='descending' AND :order='date' THEN c1.transaction_date  END DESC,
        CASE WHEN :sort='descending' AND :order='transaction amount' THEN c1.transaction_amount END DESC  
    
        
''',
                              sort=sort,
                              order=order))
    def get_all_view(order,sort,view): #just gets everyting in the table
        return (app.db.execute('''
SELECT *
FROM Committee c1
WHERE c1.cycle=:view
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
                              order=order))
    def get_all_type(order,sort,type): #just gets everyting in the table
        return (app.db.execute('''
SELECT *
FROM Committee c1
WHERE c1.ctype=:type
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
                              order=order))

    def get_all_view_type(order,sort,view,type): #just gets everyting in the table
        return (app.db.execute('''
SELECT *
FROM Committee c1
WHERE c1.cycle=:view AND c1.ctype=:type
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
        CASE WHEN :sort='ascending' AND :order='transaction amount' THEN transaction_amount  END ASC,
        CASE WHEN :sort='descending' AND :order='election cycle' THEN cycle  END DESC,
        CASE WHEN :sort='descending' AND :order='transaction amount' THEN transaction_amount END DESC 
    
        
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
        return rows


    

    @staticmethod
    def get_all_range(from_date, to_date, sort_by,aord,cid): #gets everything in the table given a range of dates
        rows = app.db.execute('''
            SELECT *
            FROM Committee
            WHERE CAST (year AS INTEGER) >=:y1 AND CAST (year AS INTEGER)<=:y2 AND cid = :cid
            ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN did END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN year END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN transaction_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN transaction_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN did END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN year END DESC
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              cid=cid
                              )
        return [Committee (*row) for row in rows]



    @staticmethod
    def get_all_to_entity_range(to_entity, from_date, to_date, sort_by,aord,cid): #gets everything in the table going to to_entity
        rows = app.db.execute('''
            SELECT *
                  FROM Committee
            WHERE to_entity = :to_entity
            AND CAST (year AS INTEGER)>=:y1 AND CAST (year AS INTEGER)<=:y2 and cid = :cid
            ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN did END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN year END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN transaction_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN transaction_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN did END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN year END DESC
            ''',
                              to_entity=to_entity,
                              from_date=from_date,
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              cid=cid
                              )
        return [Committee (*row) for row in rows]
    
    @staticmethod
    def get_all_involving(search_entity,from_date,to_date, sort_by,aord,cid):
        rows = app.db.execute('''
            SELECT *        FROM Committee
            WHERE cid = :cid AND ( name_contributor=:entity) AND CAST (year AS INTEGER)>=:y1 AND CAST (year AS INTEGER)<=:y2
           ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN did END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN year END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN transaction_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN transaction_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN did END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN year END DESC
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
    def get_sum_all (from_date,to_date,cid):
        rows = app.db.execute('''
            SELECT SUM(transaction_amount)
            FROM Committee
            WHERE CAST (year AS INTEGER)>=:y1 AND CAST (year AS INTEGER)<=:y2 AND cid = :cid
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
            WHERE CAST (year AS INTEGER)>=:y1 AND CAST (year AS INTEGER)<=:y2 AND cid = :cid AND (name_contributor=:entity) 
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              entity=any_ent,
                              cid=cid
                              )
        return rows[0]
    
    @staticmethod
    def get_sum_to (to_ent,from_date,to_date,cid):
        rows = app.db.execute('''
            SELECT SUM(transaction_amount)
            FROM Committee
            WHERE CAST (year AS INTEGER)>=:y1 AND CAST (year AS INTEGER)<=:y2 AND name_contributor=:to_ent AND cid = :cid
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              to_ent=to_ent,
                              cid=cid
                              )
        return rows[0]