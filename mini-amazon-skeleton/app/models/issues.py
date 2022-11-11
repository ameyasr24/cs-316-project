from flask import current_app as app

class Issues:
    def __init__(self, legislation_number, legislation_URL, title, sponsor, cosponsor1, cosponsor2, cosponsor3, cosponsor4, cosponsor5, subject1, subject2, subject3, subject4, subject5):
        self.legislation_number = legislation_number
        self.legislation_URL = legislation_URL
        self.title = title
        self.sponsor = sponsor
        self.cosponsor1 = cosponsor1
        self.cosponsor2 = cosponsor2
        self.cosponsor3 = cosponsor3
        self.cosponsor4 = cosponsor4
        self.cosponsor5 = cosponsor5
        self.subject1 = subject1
        self.subject2 = subject2
        self.subject3 = subject3
        self.subject4 = subject4
        self.subject5 = subject5

    @staticmethod 
    def get(legislation_number): #gets by id value
        rows = app.db.execute('''
SELECT legislation_number, legislation_URL, title, sponsor, cosponsor1, cosponsor2, cosponsor3, cosponsor4, cosponsor5, subject1, subject2, subject3, subject4, subject5
FROM Senate_Legislation_Topics
WHERE legislation_number = :legislation_number
''',
                              legislation_number=legislation_number)
        return Issues(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(): #just gets everyting in the table
        rows = app.db.execute('''
SELECT legislation_number, legislation_URL, title, sponsor, cosponsor1, cosponsor2, cosponsor3, cosponsor4, cosponsor5, subject1, subject2, subject3, subject4, subject5
FROM Senate_Legislation_Topics
''',
                              )
        return [Issues(*row) for row in rows]

    @staticmethod
    def get_all_issue(subject): #filtering for a specific issue
        rows = app.db.execute('''
            SELECT legislation_number, legislation_URL, title, sponsor, cosponsor1, cosponsor2, cosponsor3, cosponsor4, cosponsor5, subject1, subject2, subject3, subject4, subject5
            FROM Senate_Legislation_Topics
            WHERE subject1=:subject OR 
            subject2=:subject OR
            subject3=:subject OR
            subject4=:subject OR
            subject5=:subject
            ''',
                            
                              subject=subject,
                              )
        return [Issues(*row) for row in rows]

    @staticmethod
    def get_all_issue_politician(subject, senator): #filtering for a specific issue
        rows = app.db.execute('''
            SELECT legislation_number, legislation_URL, title, sponsor, cosponsor1, cosponsor2, cosponsor3, cosponsor4, cosponsor5, subject1, subject2, subject3, subject4, subject5
            FROM Senate_Legislation_Topics
            WHERE (subject1=:subject OR 
            subject2=:subject OR
            subject3=:subject OR
            subject4=:subject OR
            subject5=:subject) AND
            (sponsor=:senator OR 
            cosponsor1=:senator OR
            cosponsor2=:senator OR
            cosponsor3=:senator OR
            cosponsor4=:senator OR
            cosponsor5=:senator
            )
            ''',
                              subject=subject,
                              senator=senator
                              )
        return [Issues(*row) for row in rows]

    
            # WHERE LIKE(subject1, @subject) OR 
            # LIKE(subject2, :subject) OR
            # LIKE(subject3, :subject) OR
            # LIKE(subject4, :subject) OR
            # LIKE(subject5, :subject)

# class Issues:
#     def __init__(self, id, policy_category, politician, donor, donor_industry, donation_amount, yr, legislation, vote, link):
#         self.id = id
#         self.policy_category = policy_category
#         self.politician = politician
#         self.donor = donor
#         self.donor_industry = donor_industry
#         self.donation_amount = donation_amount
#         self.yr = yr
#         self.legislation = legislation
#         self.vote = vote
#         self.link = link


#     @staticmethod 
#     def get(id): #gets by id value
#         rows = app.db.execute('''
# SELECT id, policy_category, politician, donor, donor_industry, donation_amount, yr, legislation, vote, link
# FROM Issues
# WHERE id = :id
# ''',
#                               id=id)
#         return Issues(*(rows[0])) if rows is not None else None

#     @staticmethod
#     def get_all(): #just gets everyting in the table
#         rows = app.db.execute('''
# SELECT id, policy_category, politician, donor, donor_industry, donation_amount, yr, legislation, vote, link
# FROM Issues
# ''',
#                               )
#         return [Issues(*row) for row in rows]

#     @staticmethod
#     def get_all_issue(issue): #filtering for a specific issue
#         rows = app.db.execute('''
#             SELECT id, policy_category, politician, donor, donor_industry, donation_amount, yr, legislation, vote, link
#             FROM Issues
#             WHERE policy_category=:issue_category
#             ''',
                              
#                               issue_category=issue,
#                               )
#         return [Issues(*row) for row in rows]

   