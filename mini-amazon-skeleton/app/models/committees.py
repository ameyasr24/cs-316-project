from flask import current_app as app


class Committees:
    def __init__(self, cid, from_entity, to_entity, donation_amount, from_category, to_category, yr):
        self.cid = cid
        self.from_entity = from_entity
        self.to_entity = to_entity
        self.donation_amount = donation_amount
        self.from_category = from_category
        self.to_category = to_category
        self.yr = yr


    @staticmethod 
    def get(cid): #gets everything by cid value
        rows = app.db.execute('''
SELECT cid, from_entity, to_entity, donation_amount, from_category, to_category, yr
FROM Committees
WHERE cid = :cid
''',
                              cid=cid)
        return Committees(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(sort_by, aord): #just gets everyting in the table
        rows = app.db.execute('''
SELECT cid, from_entity, to_entity, donation_amount,  from_category, to_category, yr
FROM Committees 
ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN cid END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN cid END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
        
''',
                              s=sort_by,
                              AD=aord,
                              )
        return [Committees(*row) for row in rows]

    @staticmethod
    def get_all_range(from_date, to_date, sort_by,aord): #gets everything in the table given a range of dates
        rows = app.db.execute('''
            SELECT cid, from_entity, to_entity, donation_amount, from_category, to_category, yr
            FROM Committees
            WHERE yr>=:y1 AND yr<=:y2
            ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN cid END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN cid END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              )
        return [Committees(*row) for row in rows]

    @staticmethod
    def get_all_from_to_range(to_entity, from_entity,from_date, to_date, sort_by,aord): #gets everything in the table going to to_entity and from from_entity
        rows = app.db.execute('''
            SELECT cid, from_entity, to_entity, donation_amount, from_category, to_category, yr
            FROM Committees
            WHERE to_entity = :to_entity AND from_entity=:from_entity 
            AND yr>=:y1 AND yr<=:y2
           ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN cid END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN cid END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
            ''',
                              to_entity=to_entity,
                              from_entity=from_entity,
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              )
        return [Committees(*row) for row in rows]

    @staticmethod
    def get_all_to_entity_range(to_entity, from_date, to_date, sort_by,aord): #gets everything in the table going to to_entity
        rows = app.db.execute('''
            SELECT cid, from_entity, to_entity, donation_amount,  from_category, to_category, yr
            FROM Committees
            WHERE to_entity = :to_entity
            AND yr>=:y1 AND yr<=:y2
            ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN cid END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN cid END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
            ''',
                              to_entity=to_entity,
                              from_date=from_date,
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              )
        return [Committees(*row) for row in rows]
    @staticmethod
    def get_all_from_entity_range(from_entity, from_date, to_date, sort_by,aord): #gets everything in the table going from from_entity
        rows = app.db.execute('''
            SELECT cid, from_entity, to_entity, donation_amount,  from_category, to_category, yr
            FROM Committees
            WHERE from_entity = :from_entity
            AND yr>=:y1 AND yr<=:y2
            ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN cid END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN cid END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
            ''',
                              from_entity=from_entity,
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              )
        return [Committees(*row) for row in rows]
    
    @staticmethod
    def get_all_involving(search_entity,from_date,to_date, sort_by,aord):
        rows = app.db.execute('''
            SELECT cid, from_entity, to_entity, donation_amount,  from_category, to_category, yr
            FROM Committees
            WHERE from_entity = :entity 
            OR to_entity=:entity AND yr>=:y1 AND yr<=:y2
           ORDER BY CASE WHEN :AD='ascending' AND :s='ID' THEN cid END ASC,
        CASE WHEN :AD='ascending' AND :s='year' THEN yr END ASC,
        CASE WHEN :AD='ascending' AND :s='donation amount' THEN donation_amount END ASC,
        CASE WHEN :AD='descending' AND :s='donation amount' THEN donation_amount END DESC,
        CASE WHEN :AD='descending' AND :s='ID' THEN cid END DESC,
        CASE WHEN :AD='descending' AND :s='year' THEN yr END DESC
            ''',
                              entity=search_entity,
                              y1=from_date,
                              y2=to_date,
                              s=sort_by,
                              AD=aord,
                              )
        return [Committees(*row) for row in rows]
       