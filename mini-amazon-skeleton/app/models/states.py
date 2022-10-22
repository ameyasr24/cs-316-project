from flask import current_app as app


class State:
    def __init__(self, id, state_id, year, candidate_name, party, incumbent_status, total_receipts, percent_vote):
        self.id = id
        self.state_id = state_id
        self.year = year
        self.candidate_name = candidate_name
        self.party = party
        self.incumbent_status = incumbent_status
        self.total_receipts = total_receipts
        self.percent_vote = percent_vote
    
    @staticmethod
    def get_all(state_abb):
        rows = app.db.execute('''
SELECT *
FROM States
WHERE state_id = :state_abb
''',
                            state_abb = state_abb)
        # print(state_abb)
        return [State(*row) for row in rows]
