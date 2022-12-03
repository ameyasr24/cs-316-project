from flask import current_app as app


class Committee:
    def __init__(self, cid, cname, ctype, cdesignation,cfilingfreq, total_receipts,
    entity_tp  ,
    transfers_from_aff  ,
    indiv_contrib,
    other_pac_contrib,
    cand_contrib,
    cand_loans,
    ttl_loans,
    ttl_disburse,
    transfers_to_aff,
    indv_refunds ,
    other_pac_refunds,
    cand_loan_repay,
    loan_repay,
    coh_bop,
    coh_cop,
    debts_owed_by,
    nonfed_transfers_received,
    contrib_to_other_comm,
    ind_exp,
    pty_coord_exp,
    cvg_end_dt,election_cycle):
        self.cid = cid
        self.cname = cname
        self.ctype = ctype
        self.cdesignation=cdesignation
        self.cfilingfreq=cfilingfreq
        self.total_receipts=total_receipts
        self.entity_tp=entity_tp
        self.transfers_from_aff  =transfers_from_aff
        self.indiv_contrib=indiv_contrib
        self.other_pac_contrib=other_pac_contrib
        self.cand_contrib=cand_contrib
        self.cand_loans=cand_loans
        self.ttl_loans=ttl_loans
        self.ttl_disburse=ttl_disburse
        self.transfers_to_aff=transfers_to_aff
        self.indv_refunds=indv_refunds
        self.other_pac_refunds=other_pac_refunds
        self.cand_loan_repay=cand_loan_repay
        self.loan_repay=loan_repay
        self.coh_bop=coh_bop
        self.coh_cop=coh_cop
        self.debts_owed_by=debts_owed_by
        self.nonfed_transfers_received=nonfed_transfers_received
        self.contrib_to_other_comm=contrib_to_other_comm
        self.ind_exp=ind_exp
        self.pty_coord_exp=pty_coord_exp
        self.cvg_end_dt=cvg_end_dt
        self.election_cycle=election_cycle


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
SELECT cid, cname, ctype, cdesignation,cfilingfreq, total_receipts,
    entity_tp  ,
    transfers_from_aff  ,
    indiv_contrib,
    other_pac_contrib,
    cand_contrib,
    cand_loans,
    ttl_loans,
    ttl_disburse,
    transfers_to_aff,
    indv_refunds ,
    other_pac_refunds,
    cand_loan_repay,
    loan_repay,
    coh_bop,
    coh_cop,
    debts_owed_by,
    nonfed_transfers_received,
    contrib_to_other_comm,
    ind_exp,
    pty_coord_exp,
    cvg_end_dt,cycle
FROM Committee 
ORDER BY cname
        
''',
                              
                              )
        return [Committee(*row) for row in rows]

    @staticmethod
    def get_comm(name):
        rows = app.db.execute('''
SELECT cname, total_receipts
FROM Committee  WHERE cname=:name
ORDER BY cname 
        
''',
                              
                              name=name)
        return [Committee(*row) for row in rows]
    @staticmethod
    def get_name(cid):
        rows = app.db.execute('''
SELECT cname
FROM Committee  WHERE cid=:cid
        
''',
                              
                              cid=cid)
        return rows[0]