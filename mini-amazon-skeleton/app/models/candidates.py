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
        SELECT cm.bioname AS bioname, vcc.descr AS descr, cvd.congress AS congress, cvd.vote_date AS vote_date, cvd.vote_desc AS vote_desc, cvd.dtl_desc AS dtl_desc, cvd.vote_result AS vote_result
        FROM Candidate_Member_Votes cmv, Vote_Cast_Codes vcc, Candidate_Vote_Data cvd, Candidate_Members cm
        WHERE cm.icpsr = :cid AND cm.icpsr = cmv.icpsr AND cvd.congress = cmv.congress AND cvd.rollnumber = cmv.rollnumber
        AND cmv.cast_code = vcc.cast_code
        ORDER BY cvd.vote_date;
        ''',
                              cid=cid)
        if len(rows) > 0:
            return rows
        return "oops"

    def get_all_candidates():
        rows = app.db.execute('''
        SELECT DISTINCT c.candidate_name
        FROM Candidate_Members c
        ORDER BY c.candidate_name''')
        if len(rows) > 0:
            return rows
        return "oops"