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

   