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
        SELECT DISTINCT cm.bioname AS bioname, vcc.descr AS descr, cvd.congress AS congress, cvd.rollnumber AS rollnumber, cvd.vote_date AS vote_date, cvd.vote_desc AS vote_desc, cvd.dtl_desc AS dtl_desc, cvd.vote_result AS vote_result, cpc.party AS party, cm.state_abbrev AS state
        FROM Candidate_Member_Votes cmv, Vote_Cast_Code vcc, Candidate_Vote_Data cvd, Candidate_Members cm, Candidate_Party_Codes cpc
        WHERE CAST(cm.icpsr as INTEGER) = :cid AND cm.icpsr = cmv.icpsr AND cvd.congress = cmv.congress AND cvd.rollnumber = cmv.rollnumber AND cm.chamber = 'Senate'
        AND cmv.cast_code = vcc.cast_code AND cpc.party_code = cm.party_code
        ORDER BY cvd.vote_date;
        ''',
                              cid=cid)
        if len(rows) > 0:
            return rows
        return "oops"

    def get_all_candidates():
        rows = app.db.execute('''
        SELECT DISTINCT c.bioname, CAST(c.icpsr as INTEGER), cpc.party
        FROM Candidate_Members c, Candidate_Party_Codes cpc
        WHERE c.chamber = 'Senate' AND cpc.party_code = c.party_code
        ORDER BY c.bioname''')
        if len(rows) > 0:
            return rows
        return "oops"

    def get_all_congresses(cid):
        rows = app.db.execute('''
        SELECT DISTINCT cvd.congress AS congress
        FROM Candidate_Member_Votes cmv, Vote_Cast_Code vcc, Candidate_Vote_Data cvd, Candidate_Members cm
        WHERE CAST(cm.icpsr as INTEGER) = :cid AND cm.icpsr = cmv.icpsr AND cvd.congress = cmv.congress AND cvd.rollnumber = cmv.rollnumber AND cm.chamber = 'Senate'
        AND cmv.cast_code = vcc.cast_code
        ORDER BY cvd.congress;
        ''',
                              cid=cid)
        return rows

    def get_all_vote_types(cid):
        rows = app.db.execute('''
        SELECT DISTINCT vcc.descr AS descr
        FROM Candidate_Member_Votes cmv, Vote_Cast_Code vcc, Candidate_Vote_Data cvd, Candidate_Members cm
        WHERE CAST(cm.icpsr as INTEGER) = :cid AND cm.icpsr = cmv.icpsr AND cvd.congress = cmv.congress AND cvd.rollnumber = cmv.rollnumber AND cm.chamber = 'Senate'
        AND cmv.cast_code = vcc.cast_code
        ORDER BY vcc.descr;
        ''',
                              cid=cid)
        return rows

    def get_all_vote_years(cid): # gets all votes by a specific candidate
        rows = app.db.execute('''
        SELECT DISTINCT CAST(EXTRACT(YEAR FROM cvd.vote_date) AS INTEGER) AS vote_year
        FROM Candidate_Member_Votes cmv, Vote_Cast_Code vcc, Candidate_Vote_Data cvd, Candidate_Members cm
        WHERE CAST(cm.icpsr as INTEGER) = :cid AND cm.icpsr = cmv.icpsr AND cvd.congress = cmv.congress AND cvd.rollnumber = cmv.rollnumber AND cm.chamber = 'Senate'
        AND cmv.cast_code = vcc.cast_code
        ORDER BY vote_year;
        ''',
                              cid=cid)
        return rows

    def get_all_votes_for_congress(cid, congress): # gets all votes by a specific candidate
        rows = app.db.execute('''
        SELECT DISTINCT cm.bioname AS bioname, vcc.descr AS descr, cvd.congress AS congress, cvd.rollnumber AS rollnumber, cvd.vote_date AS vote_date, cvd.vote_desc AS vote_desc, cvd.dtl_desc AS dtl_desc, cvd.vote_result AS vote_result, cpc.party AS party, cm.state_abbrev AS state
        FROM Candidate_Member_Votes cmv, Vote_Cast_Code vcc, Candidate_Vote_Data cvd, Candidate_Members cm, Candidate_Party_Codes cpc
        WHERE CAST(cm.icpsr as INTEGER) = :cid AND cm.icpsr = cmv.icpsr AND cvd.congress = cmv.congress AND cvd.rollnumber = cmv.rollnumber AND cm.chamber = 'Senate'
        AND cmv.cast_code = vcc.cast_code AND cvd.congress = :congress AND cpc.party_code = cm.party_code
        ORDER BY cvd.vote_date;
        ''',
                              cid=cid, congress=congress)
        if len(rows) > 0:
            return rows
        return "oops"

    def get_all_votes_for_votetype(cid, votetype): # gets all votes by a specific candidate
        rows = app.db.execute('''
        SELECT DISTINCT cm.bioname AS bioname, vcc.descr AS descr, cvd.congress AS congress, cvd.rollnumber AS rollnumber, cvd.vote_date AS vote_date, cvd.vote_desc AS vote_desc, cvd.dtl_desc AS dtl_desc, cvd.vote_result AS vote_result, cpc.party AS party, cm.state_abbrev AS state
        FROM Candidate_Member_Votes cmv, Vote_Cast_Code vcc, Candidate_Vote_Data cvd, Candidate_Members cm, Candidate_Party_Codes cpc
        WHERE CAST(cm.icpsr as INTEGER) = :cid AND cm.icpsr = cmv.icpsr AND cvd.congress = cmv.congress AND cvd.rollnumber = cmv.rollnumber AND cm.chamber = 'Senate'
        AND cmv.cast_code = vcc.cast_code AND vcc.descr = :votetype AND cpc.party_code = cm.party_code
        ORDER BY cvd.vote_date;
        ''',
                              cid=cid, votetype=votetype)
        if len(rows) > 0:
            return rows
        return "oops"

    def get_all_votes_for_voteyear(cid, voteyear): # gets all votes by a specific candidate
        rows = app.db.execute('''
        SELECT DISTINCT cm.bioname AS bioname, vcc.descr AS descr, cvd.congress AS congress, cvd.rollnumber AS rollnumber, cvd.vote_date AS vote_date, cvd.vote_desc AS vote_desc, cvd.dtl_desc AS dtl_desc, cvd.vote_result AS vote_result, cpc.party AS party, cm.state_abbrev AS state
        FROM Candidate_Member_Votes cmv, Vote_Cast_Code vcc, Candidate_Vote_Data cvd, Candidate_Members cm, Candidate_Party_Codes cpc
        WHERE CAST(cm.icpsr as INTEGER) = :cid AND cm.icpsr = cmv.icpsr AND cvd.congress = cmv.congress AND cvd.rollnumber = cmv.rollnumber AND cm.chamber = 'Senate'
        AND cmv.cast_code = vcc.cast_code AND CAST(EXTRACT(YEAR FROM cvd.vote_date) AS INTEGER) = :voteyear AND cpc.party_code = cm.party_code
        ORDER BY cvd.vote_date;
        ''',
                              cid=cid, voteyear=voteyear)
        if len(rows) > 0:
            return rows
        return "oops"

class Candidate_Donations:
    def __init__(self, id, contributor, donation_amount, donation_date):
        self.id = id
        self.contributor = contributor
        self.donation_amount = donation_amount
        self.donation_date = donation_date

    @staticmethod 
    def get_all_donations(cid): # gets all donations to a specific candidate
        rows = app.db.execute('''
        SELECT DISTINCT contributor, donation_amount, donation_date
        FROM Candidate_Donations
        WHERE icpsr = :cid
        ORDER BY donation_amount DESC;
        ''',
                              cid=cid)
        if len(rows) > 0:
            return rows
        return "oops"

    def grouped_donations(cid):
        rows = app.db.execute('''
        SELECT DISTINCT contributor, SUM(donation_amount) AS donation_amoun, COUNT(donation_amount) AS number_donations
        FROM Candidate_Donations
        WHERE icpsr = :cid
        GROUP BY contributor
        ORDER BY donation_amoun DESC;
        ''',
                              cid=cid)
        if len(rows) > 0:
            return rows
        return "oops"