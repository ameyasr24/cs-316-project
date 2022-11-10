from flask import current_app as app


class Committee:
    def __init__(self, cid, cname, type):
        self.cid = cid
        self.cname = cname
        self.type = type

    @staticmethod 
    def get(cid): #gets everything by cid value
        rows = app.db.execute('''
SELECT cname
FROM Committee
WHERE cid = :cid
''',
                              cid=cid)
        return Committee(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(): #just gets everyting in the table
        rows = app.db.execute('''
SELECT cid, cname,type
FROM Committee 
ORDER BY cid
        
''',
                              
                              )
        return [Committee(*row) for row in rows]

    @staticmethod
    def get_comm(name):
        rows = app.db.execute('''
SELECT cid, cname,type
FROM Committee  WHERE cname=:name
ORDER BY cid 
        
''',
                              
                              name=name)
        return [Committee(*row) for row in rows]