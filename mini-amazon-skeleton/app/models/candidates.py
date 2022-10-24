from flask import current_app as app

class Candidate_Vote:
    def __init__(self, id, state_id, candidate_name, candidate_vote, vote_id, vote_date, vote_result, vote_description):
        self.id = id
        self.state_id = state_id
        self.candidate_name = candidate_name
        self.candidate_vote = candidate_vote
        self.vote_id = vote_id
        self.vote_date = vote_date
        self.vote_result = vote_result
        self.vote_description = vote_description

    @staticmethod 
    def get_all_votes(cid): # gets all votes by a specific candidate
        rows = app.db.execute('''
        SELECT candidate_name, candidate_vote, vote_date, vote_description, vote_result
        FROM Candidate_Vote
        WHERE id = :cid
        ORDER BY vote_date
        ''',
                              cid=cid)
        if len(rows) > 0:
            return rows
        return "oops"

    def get_all_candidates():
        rows = app.db.execute('''
        SELECT DISTINCT c.id, c.candidate_name
        FROM Candidate_Vote c
        ORDER BY c.candidate_name''')
        if len(rows) > 0:
            return rows
        return "oops"