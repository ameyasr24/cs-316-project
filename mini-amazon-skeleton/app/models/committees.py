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
    def get_all(): #just gets everyting in the table
        rows = app.db.execute('''
SELECT cid, from_entity, to_entity, donation_amount,  from_category, to_category, yr
FROM Committees
''',
                              )
        return [Committees(*row) for row in rows]

    @staticmethod
    def get_all_range(from_date, to_date): #gets everything in the table going to to_entity
        rows = app.db.execute('''
            SELECT cid, from_entity, to_entity, donation_amount, from_category, to_category, yr
            FROM Committees
            WHERE yr>=:y1 AND yr<=:y2
            ''',
                              
                              y1=from_date,
                              y2=to_date,
                              )
        return [Committees(*row) for row in rows]

    @staticmethod
    def get_all_from_to_range(to_entity, from_entity,from_date, to_date): #gets everything in the table going to to_entity
        rows = app.db.execute('''
            SELECT cid, from_entity, to_entity, donation_amount, from_category, to_category, yr
            FROM Committees
            WHERE to_entity = :to_entity AND from_entity=:from_entity 
            AND yr>=:y1 AND yr<=:y2
            ''',
                              to_entity=to_entity,
                              from_entity=from_entity,
                              y1=from_date,
                              y2=to_date,
                              )
        return [Committees(*row) for row in rows]

    @staticmethod
    def get_all_to_entity_range(to_entity, from_date, to_date): #gets everything in the table going to to_entity given a particular time period
        rows = app.db.execute('''
            SELECT cid, from_entity, to_entity, donation_amount,  from_category, to_category, yr
            FROM Committees
            WHERE to_entity = :to_entity
            AND yr>=:y1 AND yr<=:y2
            ''',
                              to_entity=to_entity,
                              from_date=from_date,
                              y1=from_date,
                              y2=to_date,
                              )
        return [Committees(*row) for row in rows]
    @staticmethod
    def get_all_from_entity_range(from_entity, from_date, to_date): #gets everything in the table going from from_entity given a particular time period
        rows = app.db.execute('''
            SELECT cid, from_entity, to_entity, donation_amount,  from_category, to_category, yr
            FROM Committees
            WHERE from_entity = :from_entity
            AND yr>=:y1 AND yr<=:y2
            ''',
                              from_entity=from_entity,
                              y1=from_date,
                              y2=to_date
                              )
        return [Committees(*row) for row in rows]
    @staticmethod
    def sort_by_cid():
        rows = app.db.execute('''
            SELECT *
            FROM Committees
            ORDER BY cid ASC
            ''',
                              )
        return [Committees(*row) for row in rows]
    @staticmethod
    def sort_by_date_asc():
        rows = app.db.execute('''
            SELECT *
            FROM Committees
            ORDER BY yr ASC
            ''',
                              )
        return [Committees(*row) for row in rows]
    @staticmethod
    def sort_by_date_desc():
        rows = app.db.execute('''
            SELECT *
            FROM Committees
            ORDER BY yr DESC
            ''',
                              )
        return [Committees(*row) for row in rows]