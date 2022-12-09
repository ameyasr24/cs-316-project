from flask import current_app as app


class State: 
    def __init__(self, state_id, year, candidate_name, party, incumbent_status, total_receipts, percent_vote):
        self.state_id = state_id
        self.year = year
        self.candidate_name = candidate_name
        self.party = party
        self.incumbent_status = incumbent_status
        self.total_receipts = total_receipts
        self.percent_vote = percent_vote

   #return all of the data from a specific state
    @staticmethod
    def get_all(state_abb):
        rows = app.db.execute('''
WITH r AS (SELECT cand_office_st, SPLIT_PART(cvg_end_dt::VARCHAR(10), '-', 1) AS year, SPLIT_PART(cand_name, ',', 1) AS last_name, SPLIT_PART(cand_name, ' ', 2) AS first_name, cand_pty_affiliation, cand_ici, ttl_receipts
FROM Receipts),
s AS (SELECT SPLIT_PART(candidate, ' ', 1) AS first_name, SPLIT_PART(candidate, ' ', 2) AS last_name1, SPLIT_PART(candidate, ' ', 3) AS last_name2, candidate, year, (candidatevotes*100)/(totalvotes) AS percent_votes
FROM Senate_Results)
SELECT DISTINCT r.cand_office_st, s.year, s.candidate, r.cand_pty_affiliation, r.cand_ici, r.ttl_receipts, s.percent_votes
FROM s JOIN r
ON s.year = r.year::INT
AND s.first_name = r.first_name
AND (s.last_name1 = r.last_name
OR s.last_name2 = r.last_name)
WHERE cand_office_st = :state_abb
ORDER BY s.year DESC
''',
                            state_abb = state_abb)
        return [State(*row) for row in rows]

    #return unique years
    @staticmethod
    def get_unique_years(state_abb): 
        rows = app.db.execute('''
WITH r AS (SELECT cand_office_st, SPLIT_PART(cvg_end_dt::VARCHAR(10), '-', 1) AS year, SPLIT_PART(cand_name, ',', 1) AS last_name, SPLIT_PART(cand_name, ' ', 2) AS first_name, cand_pty_affiliation, cand_ici, ttl_receipts
FROM Receipts),
s AS (SELECT SPLIT_PART(candidate, ' ', 1) AS first_name, SPLIT_PART(candidate, ' ', 2) AS last_name1, SPLIT_PART(candidate, ' ', 3) AS last_name2, candidate, year, (candidatevotes*100)/(totalvotes) AS percent_votes
FROM Senate_Results)
SELECT DISTINCT r.cand_office_st, s.year, s.year, r.year, r.year, r.year, s.year
FROM s JOIN r
ON s.year = r.year::INT
AND s.first_name = r.first_name
AND (s.last_name1 = r.last_name
OR s.last_name2 = r.last_name)
WHERE cand_office_st = :state_abb
ORDER BY s.year
''',
                            state_abb = state_abb)
        return [State(*row) for row in rows]

    #return data from a specific year's race in a specific state
    @staticmethod
    def get_all_year(state_abb, year): 
        rows = app.db.execute('''
WITH r AS (SELECT cand_office_st, SPLIT_PART(cvg_end_dt::VARCHAR(10), '-', 1) AS year, SPLIT_PART(cand_name, ',', 1) AS last_name, SPLIT_PART(cand_name, ' ', 2) AS first_name, cand_pty_affiliation, cand_ici, ttl_receipts
FROM Receipts),
s AS (SELECT SPLIT_PART(candidate, ' ', 1) AS first_name, SPLIT_PART(candidate, ' ', 2) AS last_name1, SPLIT_PART(candidate, ' ', 3) AS last_name2, candidate, year, (candidatevotes*100)/(totalvotes) AS percent_votes
FROM Senate_Results)
SELECT r.cand_office_st, s.year, s.candidate, r.cand_pty_affiliation, r.cand_ici, r.ttl_receipts, s.percent_votes
FROM s JOIN r
ON s.year = r.year::INT
AND s.first_name = r.first_name
AND (s.last_name1 = r.last_name
OR s.last_name2 = r.last_name) 
WHERE cand_office_st = :state_abb
AND s.year = :year
''',
                            state_abb = state_abb,
                            year = year)
        return [State(*row) for row in rows]