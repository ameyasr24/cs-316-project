from flask import current_app as app


class Committee_Donations:
    def __init__(self, did, from_entity, to_entity, donation_amount, from_category, to_category, yr,cid):
        self.did = did
        self.from_entity = from_entity
        self.to_entity = to_entity
        self.donation_amount = donation_amount
        self.from_category = from_category
        self.to_category = to_category
        self.yr = yr
        self.cid = cid


    @staticmethod 
    def get(cid,sort_by,aord): #gets everything by did value
        rows = app.db.execute('''
SELECT did, from_entity, to_entity, donation_amount, from_category, to_category, yr,cid
FROM Committee_Donations
WHERE cid = :cid
ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN did END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN did END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
        
''',
                              s=sort_by,
                              AD=aord,
                              cid=cid
                              )

        return [Committee_Donations(*row) for row in rows]

    @staticmethod
    def get_all(sort_by, aord): #just gets everyting in the table*******not used
        rows = app.db.execute('''
SELECT did, from_entity, to_entity, donation_amount,  from_category, to_category, yr,cid
FROM Committee_Donations WHERE cid = :cid
ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN did END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN did END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
        
''',
                              s=sort_by,
                              AD=aord,
                              cid=cid
                              )
        return [Committee_Donations(*row) for row in rows]

    @staticmethod
    def get_all_range(from_date, to_date, sort_by,aord,cid): #gets everything in the table given a range of dates
        rows = app.db.execute('''
            SELECT did, from_entity, to_entity, donation_amount, from_category, to_category, yr,cid
            FROM Committee_Donations
            WHERE yr>=:y1 AND yr<=:y2 AND cid = :cid
            ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN did END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN did END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              cid=cid
                              )
        return [Committee_Donations(*row) for row in rows]

    @staticmethod
    def get_all_from_to_range(to_entity, from_entity,from_date, to_date, sort_by,aord,cid): #gets everything in the table going to to_entity and from from_entity
        rows = app.db.execute('''
            SELECT did, from_entity, to_entity, donation_amount, from_category, to_category, yr,cid
            FROM Committee_Donations
            WHERE to_entity = :to_entity AND from_entity=:from_entity 
            AND yr>=:y1 AND yr<=:y2 AND cid = :cid
           ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN did END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN did END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
            ''',
                              to_entity=to_entity,
                              from_entity=from_entity,
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              cid=cid
                              )
        return [Committee_Donations(*row) for row in rows]

    @staticmethod
    def get_all_to_entity_range(to_entity, from_date, to_date, sort_by,aord,cid): #gets everything in the table going to to_entity
        rows = app.db.execute('''
            SELECT did, from_entity, to_entity, donation_amount,  from_category, to_category, yr,cid
            FROM Committee_Donations
            WHERE to_entity = :to_entity
            AND yr>=:y1 AND yr<=:y2 and cid = :cid
            ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN did END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN did END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
            ''',
                              to_entity=to_entity,
                              from_date=from_date,
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              cid=cid
                              )
        return [Committee_Donations(*row) for row in rows]
    @staticmethod
    def get_all_from_entity_range(from_entity, from_date, to_date, sort_by,aord,cid): #gets everything in the table going from from_entity
        rows = app.db.execute('''
            SELECT did, from_entity, to_entity, donation_amount,  from_category, to_category, yr,cid
            FROM Committee_Donations
            WHERE from_entity = :from_entity
            AND yr>=:y1 AND yr<=:y2 AND cid = :cid
            ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN did END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN did END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
            ''',
                              from_entity=from_entity,
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              cid=cid
                              )
        return [Committee_Donations(*row) for row in rows]
    
    @staticmethod
    def get_all_involving(search_entity,from_date,to_date, sort_by,aord,cid):
        rows = app.db.execute('''
            SELECT did, from_entity, to_entity, donation_amount,  from_category, to_category, yr,cid
            FROM Committee_Donations
            WHERE cid = :cid AND (from_entity = :entity OR to_entity=:entity) AND yr>=:y1 AND yr<=:y2
           ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN did END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN did END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
            ''',
                              entity=search_entity,
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              cid=cid
                              )
        return [Committee_Donations(*row) for row in rows]

    @staticmethod
    def get_sum_all (from_date,to_date,cid):
        rows = app.db.execute('''
            SELECT SUM(donation_amount)
            FROM Committee_Donations
            WHERE yr>=:y1 AND yr<=:y2 AND cid = :cid
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              cid=cid
                              )
        return rows[0]
    @staticmethod
    def get_sum_involving (any_ent, from_date,to_date,cid):
        rows = app.db.execute('''
            SELECT SUM(donation_amount)
            FROM Committee_Donations
            WHERE yr>=:y1 AND yr<=:y2 AND cid = :cid AND (from_entity = :entity  
            OR to_entity=:entity) 
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              entity=any_ent,
                              cid=cid
                              )
        return rows[0]
    @staticmethod
    def get_sum_from_to (from_ent,to_ent,from_date,to_date,cid):
        rows = app.db.execute('''
            SELECT SUM(donation_amount)
            FROM Committee_Donations
            WHERE yr>=:y1 AND yr<=:y2 AND from_entity = :from_ent  
            AND to_entity=:to_ent AND cid = :cid
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              from_ent=from_ent,
                              to_ent=to_ent,
                              cid=cid
                              )
        return rows[0]
    @staticmethod
    def get_sum_from (from_ent, from_date,to_date,cid):
        rows = app.db.execute('''
            SELECT SUM(donation_amount)
            FROM Committee_Donations
            WHERE yr>=:y1 AND yr<=:y2 AND from_entity = :from_ent AND cid = :cid
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              from_ent=from_ent,
                              cid=cid
                              )
        return rows[0]
    @staticmethod
    def get_sum_to (to_ent,from_date,to_date,cid):
        rows = app.db.execute('''
            SELECT SUM(donation_amount)
            FROM Committee_Donations
            WHERE yr>=:y1 AND yr<=:y2 AND to_entity=:to_ent AND cid = :cid
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              to_ent=to_ent,
                              cid=cid
                              )
        return rows[0]