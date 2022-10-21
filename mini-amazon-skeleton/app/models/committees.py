from flask import current_app as app


class Committee:
    def __init__(self, id, from_entity, to_entity,donation_amount,from_category,to_category, year):
        self.id = id
        self.from_entity = from_entity
        self.to_entity = to_entity
        self.donation_amount = donation_amount
        self.from_category=from_category
        self.to_category=to_category
        self.year = year


    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, from_entity, to_entity, donation_amount, from_category, to_category, year
FROM Committees
WHERE id = :id
''',
                              id=id)
        return Committee(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, from_entity, to_entity, donation_amount, from_category, to_category, year
FROM Committees
''',
                              )
        return [Committee(*row) for row in rows]
            