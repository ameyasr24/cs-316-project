from flask import current_app as app

class Issues:
    def __init__(self, id, policy_category, politician, donor, donor_industry, donation_amount, yr, legislation, vote):
        self.id = id
        self.policy_category = policy_category
        self.politician = politician
        self.donor = donor
        self.donor_industry = donor_industry
        self.donation_amount = donation_amount
        self.yr = yr
        self.legislation = legislation
        self.vote = vote


    @staticmethod 
    def get(id): #gets by id value
        rows = app.db.execute('''
SELECT id, policy_category, politician, donor, donor_industry, donation_amount, yr, legislation, vote
FROM Issues
WHERE id = :id
''',
                              id=id)
        return Issues(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(): #just gets everyting in the table
        rows = app.db.execute('''
SELECT id, policy_category, politician, donor, donor_industry, donation_amount, yr, legislation, vote
FROM Issues
''',
                              )
        return [Issues(*row) for row in rows]

   