from flask import current_app as app


class Correlation:
    def __init__(self,id,donator_id,state_id,amount,cand_num,candidate_id,party,result,percent,issue):
        self.id = id
        self.donator_id = donator_id
        self.state_id = state_id
        self.amount = amount
        self.cand_num = cand_num
        self.candidate_id = candidate_id
        self.party = party
        self.result = result
        self.percent = percent
        self.issue = issue

    #GETS ALL DATA IN THE DATABSE
    @staticmethod
    def get_all(): 
        rows = app.db.execute('''
            SELECT *
            FROM Correlation
            ''',
                              )
        return [Correlation(*row) for row in rows]

    #GETS UNIQUE STATE NAMES
    def get_unique_state(): 
        rows = app.db.execute('''
            SELECT MAX(id),MAX(donator_id),state_id,MAX(amount),MAX(cand_num),MAX(candidate_id),MAX(party),MAX(result),MAX(percent),MAX(issue)
            FROM Correlation
            GROUP BY state_id
            ORDER BY state_id ASC
            ''',
                                                        
                              )
        return [Correlation(*row) for row in rows]



    #GETS UNIQUE CANDIDATES
    @staticmethod
    def get_unique_candidate(): 
        rows = app.db.execute('''
            SELECT MAX(id),MAX(donator_id),MAX(state_id),MAX(amount),MAX(cand_num),candidate_id,MAX(party),MAX(result),MAX(percent),MAX(issue)
            FROM Correlation
            GROUP BY candidate_id
            ''',
                                                        
                              )
        return [Correlation(*row) for row in rows]
    
    #GETS UNIQUE ISSUES
    @staticmethod
    def get_unique_issue(): 
        rows = app.db.execute('''
            SELECT MAX(id),MAX(donator_id),MAX(state_id),MAX(amount),MAX(cand_num),MAX(candidate_id),MAX(party),MAX(result),MAX(percent),issue
            FROM Correlation
            GROUP BY issue
            ''',
                                                        
                              )
        return [Correlation(*row) for row in rows]

    #BASED ON PASSED DATA, EITHER FILTER IF NOT NULL OR GET ALL IF NULL FOR RESULT STATE DONATOR CANDIDATE ISSUE AMOUNT
    def get_up_to_all(result1,state1,donator1,candidate1,issue1,amount1):
        rows = app.db.execute('''
            SELECT *
            FROM Correlation
            WHERE 
            (
                (:result1 IS NOT NULL AND result = :result1)
                OR (:result1 IS NULL)
                )
            AND (
                (:state1 IS NOT NULL AND state_id = :state1)
                OR (:state1 IS NULL)
                )
            AND (
                (:donator1 IS NOT NULL AND donator_id = :donator1)
                OR (:donator1 IS NULL)
                )
            AND (
                (:issue1 IS NOT NULL AND issue = :issue1)
                OR (:issue1 IS NULL)
                )
            AND (
                (:candidate1 IS NOT NULL AND candidate_id = :candidate1)
                OR (:candidate1 IS NULL)
                )
            AND (
                (:amount1 IS NOT NULL AND amount > :amount1)
                OR (:amount1 IS NULL)
                )

                   
            ''',
                              
                              result1 = result1,
                              state1 = state1,
                              donator1 = donator1,
                              candidate1 = candidate1,
                              issue1 = issue1,
                              amount1 = amount1                        
                              )
        return [Correlation(*row) for row in rows]


    
