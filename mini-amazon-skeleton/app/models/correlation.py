from flask import current_app as app


class Correlation:
    def __init__(self,state_id,donator_id,issue,candidate_id,committee_id,amount,passed):
        self.state_id = state_id
        self.donator_id = donator_id
        self.candidate_id = candidate_id
        self.committee_id = committee_id
        self.issue = issue
        self.amount = amount
        self.passed = passed

    @staticmethod
    def get_all(): #just gets everyting in the table
        rows = app.db.execute('''
SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
FROM Correlation
''',
                              )
        return [Correlation(*row) for row in rows]

    @staticmethod
    def get_states(state_id): #gets everything in the table going to to_entity
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE state_id = :state_id
            ''',
                              
                              state_id = state_id,                              
                              )
        return [Correlation(*row) for row in rows]
    
    def get_unique_state(): #gets everything in the table going to to_entity
        rows = app.db.execute('''
            SELECT state_id, MAX(donator_id), MAX(candidate_id), MAX(committee_id), MAX(amount), MAX(passed), MAX(issue)
            FROM Correlation
            GROUP BY state_id
            ORDER BY state_id ASC
            ''',
                                                        
                              )
        return [Correlation(*row) for row in rows]
    
    def get_unique_issue(): #gets everything in the table going to to_entity
        rows = app.db.execute('''
            SELECT MAX(passed), MAX(state_id), donator_id, MAX(candidate_id), MAX(committee_id), MAX(amount), MAX(issue)
            FROM Correlation
            GROUP BY donator_id
            ''',
                                                        
                              )
        return [Correlation(*row) for row in rows]

    @staticmethod
    def get_donator(donator): #gets everything in the table going to to_entity
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE donator_id = donator
            ''',
                              
                              donator = donator,                              
                              )
        return [Correlation(*row) for row in rows]

    @staticmethod
    def get_candidate(candidate): #gets everything in the table going to to_entity
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE candidate_id = candidate
            ''',
                              
                              candidate = candidate,                              
                              )
        return [Correlation(*row) for row in rows]

