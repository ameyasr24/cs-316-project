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
    def get_states(state_id): #gets specific state
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE state_id = :state_id
            ''',
                              
                              state_id = state_id,                              
                              )
        return [Correlation(*row) for row in rows]
    
    def get_unique_state(): #gets unique state names
        rows = app.db.execute('''
            SELECT state_id, MAX(donator_id), MAX(candidate_id), MAX(committee_id), MAX(amount), MAX(passed), MAX(issue)
            FROM Correlation
            GROUP BY state_id
            ORDER BY state_id ASC
            ''',
                                                        
                              )
        return [Correlation(*row) for row in rows]


    @staticmethod
    def get_donator(donator): #gets specific donor
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE donator_id = :donator
            ''',
                              
                              donator = donator,                              
                              )
        return [Correlation(*row) for row in rows]

    @staticmethod
    def get_candidate(candidate): #gets specific candidate
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE candidate_id = :candidate
            ''',
                              
                              candidate = candidate,                              
                              )
        return [Correlation(*row) for row in rows]

    @staticmethod
    def get_unique_candidate(): #gets list of unique candidates
        rows = app.db.execute('''
            SELECT MAX(passed), MAX(state_id), MAX(donator_id), candidate_id, MAX(committee_id), MAX(amount), MAX(issue)
            FROM Correlation
            GROUP BY candidate_id
            ''',
                                                        
                              )
        return [Correlation(*row) for row in rows]
    
    @staticmethod
    def get_issue(issue1): #gets gets specific issue
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE issue = :issue1
            ''',
                              
                              issue1 = issue1,                              
                              )
        return [Correlation(*row) for row in rows]

    @staticmethod
    def get_unique_issue(): #gets unique issues
        rows = app.db.execute('''
            SELECT MAX(passed), MAX(state_id), MAX(donator_id), MAX(candidate_id), MAX(committee_id), MAX(amount), issue
            FROM Correlation
            GROUP BY issue
            ''',
                                                        
                              )
        return [Correlation(*row) for row in rows]

    def get_passed(passed1): #gets specific passed
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE passed = :passed1
            ''',
                              
                              passed1 = passed1,                              
                              )
        return [Correlation(*row) for row in rows]

    def get_passed_issue_candidate_state(passed1,issue1,candidate1,state1): #gets passed, issue, candidate, state
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE passed = :passed1
            AND issue = :issue1
            AND candidate_id = :candidate1
            AND state_id = :state1
            ''',
                              
                              passed1 = passed1,
                              issue1 = issue1,
                              candidate1 = candidate1,
                              state1 = state1                              
                              )
        return [Correlation(*row) for row in rows]

    def get_passed_issue_candidate(passed1,issue1,candidate1): #gets passed, issue, candidate
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE passed = :passed1
            AND issue = :issue1
            AND candidate_id = :candidate1
            ''',
                              
                              passed1 = passed1,
                              issue1 = issue1,
                              candidate1 = candidate1                            
                              )
        return [Correlation(*row) for row in rows]

    def get_passed_issue_state(passed1,issue1,state1): #gets passed, issue, state
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE passed = :passed1
            AND issue = :issue1
            AND state_id = :state1
            ''',
                              
                              passed1 = passed1,
                              issue1 = issue1,
                              state1 = state1                              
                              )
        return [Correlation(*row) for row in rows]

    def get_passed_candidate_state(passed1,candidate1,state1): #gets passed candidate, state
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE passed = :passed1
            AND candidate_id = :candidate1
            AND state_id = :state1
            ''',
                              
                              passed1 = passed1,
                              candidate1 = candidate1,
                              state1 = state1                              
                              )
        return [Correlation(*row) for row in rows]

    def get_issue_candidate_state(issue1,candidate1,state1): #gets issue, candidate, state
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE issue = :issue1
            AND candidate_id = :candidate1
            AND state_id = :state1
            ''',
                              
                              issue1 = issue1,
                              candidate1 = candidate1,
                              state1 = state1                              
                              )
        return [Correlation(*row) for row in rows]

    def get_issue_candidate(issue1,candidate1): #gets issue, candidate
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE issue = :issue1
            AND candidate_id = :candidate1

            ''',
                              
                              issue1 = issue1,
                              candidate1 = candidate1,
                           
                              )
        return [Correlation(*row) for row in rows]

    def get_issue_state(issue1,state1): #gets issue, state
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE issue = :issue1
            AND state_id = :state1
            ''',
                              
                              issue1 = issue1,
                              state1 = state1                              
                              )
        return [Correlation(*row) for row in rows]    
    def get_candidate_state(candidate1,state1): #gets candidate, state
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            AND candidate_id = :candidate1
            AND state_id = :state1
            ''',
                              
                              candidate1 = candidate1,
                              state1 = state1                              
                              )
        return [Correlation(*row) for row in rows]

    def get_passed_issue(passed1,issue1): #gets passed, issue
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE passed = :passed1
            AND issue = :issue1
            ''',
                              
                              passed1 = passed1,
                              issue1 = issue1                         
                              )
        return [Correlation(*row) for row in rows]

    def get_passed_candidate(passed1,candidate1): #gets passed, candidate
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE passed = :passed1
            AND candidate_id = :candidate1
            ''',
                              
                              passed1 = passed1,
                              candidate1 = candidate1                            
                              )
        return [Correlation(*row) for row in rows]
   
    def get_passed_state(passed1,state1): #gets passed, state
        rows = app.db.execute('''
            SELECT state_id, donator_id, candidate_id, committee_id, amount, passed, issue
            FROM Correlation
            WHERE passed = :passed1
            AND state = :state1
            ''',
                              
                              passed1 = passed1,
                              issue1 = state1,                        
                              )
        return [Correlation(*row) for row in rows]
