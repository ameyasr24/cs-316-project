-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Purchases(
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);
DROP TABLE Committee;

CREATE TABLE Committee (
    tid INT NOT NULL,
    cid VARCHAR(9) NOT NULL ,
    rpt VARCHAR(3) ,
    transaction_tp VARCHAR (3),
    entity_tp  VARCHAR (200),
    name_contributor  VARCHAR (200),
    state_ VARCHAR (2),
    transaction_date date,
    transaction_amount  DECIMAL (14,2),
    other_id  VARCHAR (9),
    did  VARCHAR (32),
    year VARCHAR(4),
    cycle INT,
    cname VARCHAR(200) ,
    candidate_id  VARCHAR (9),
    candidate_name VARCHAR(200),
    PRIMARY KEY (tid)
);

CREATE TABLE Issues (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    policy_category VARCHAR(255) NOT NULL,
    politician VARCHAR(255) NOT NULL,
    donor VARCHAR(255), --!CHECK (from_category="PAC" ),--
    donor_industry VARCHAR (255), --!CHECK (to_category="candidate"),--
    donation_amount DECIMAL(20,2) NOT NULL,
    yr INT NOT NULL,
    legislation VARCHAR(255),
    vote VARCHAR(255),
    link VARCHAR(255)
);

CREATE TABLE Senate_Results (
    year INT NOT NULL,
    state VARCHAR(255) NOT NULL,
    state_po VARCHAR(2) NOT NULL,
    state_flips INT NOT NULL,
    state_cen INT NOT NULL,
    state_ic INT NOT NULL,
    office VARCHAR(255) NOT NULL,
    district VARCHAR(255) NOT NULL,
    stage VARCHAR(255) NOT NULL,
    special VARCHAR(255) NOT NULL,
    candidate VARCHAR(255) NOT NULL,
    party_detailed VARCHAR(255) NOT NULL,
    writein VARCHAR(255) NOT NULL,
    mode VARCHAR(255) NOT NULL,
    candidatevotes INT NOT NULL,
    totalvotes INT NOT NULL,
    unofficial VARCHAR(255) NOT NULL,
    version INT NOT NULL,
    party_simplified VARCHAR(255) NOT NULL
    -- PRIMARY KEY(year, candidate)
);

CREATE TABLE Receipts (
    cand_id VARCHAR(9),
    cand_name VARCHAR(200),
    cand_ici VARCHAR(1),
    pty_cd VARCHAR(1),
    cand_pty_affiliation VARCHAR(3),
    ttl_receipts MONEY,
    trans_from_auth MONEY,
    ttl_dsb MONEY,
    trans_to_auth MONEY,
    coh_bop MONEY,
    coh_cop MONEY,
    cand_contrib MONEY,
    cand_loans MONEY,
    other_loans MONEY,
    cand_loan_repay MONEY,
    other_loan_repay MONEY,
    debts_owed_by MONEY,
    ttl_indiv_contrib MONEY,
    cand_office_st VARCHAR(2),
    cand_office_district VARCHAR(2),
    spec_election VARCHAR(1),
    prim_election VARCHAR(1),
    run_election VARCHAR(1),
    gen_election VARCHAR(1),
    gen_election_percent INT,
    other_pol_cmte_contrib MONEY,
    pol_pty_contrib MONEY,
    cvg_end_dt DATE,
    indiv_refunds MONEY,
    cmte_refunds MONEY
);
    
CREATE TABLE States (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    state_id VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    candidate_name VARCHAR(255) NOT NULL,
    party VARCHAR(255) NOT NULL,
    incumbent_status VARCHAR(255) NOT NULL,
    total_receipts DECIMAL(20,2) NOT NULL,
    percent_vote DECIMAL (20,2) NOT NULL
); 

CREATE TABLE Correlation (
    state_id VARCHAR(255) NOT NULL,
    donator_id VARCHAR(255) NOT NULL,
    issue VARCHAR(255) NOT NULL,
    candidate_id VARCHAR(255) NOT NULL,
    committee_id INTEGER NOT NULL,
    amount DECIMAL(20,2) NOT NULL,
    passed VARCHAR(255) NOT NULL
);

CREATE TABLE Candidate_Member_Votes (
    congress INT NOT NULL,
    chamber VARCHAR(255) NOT NULL,
    rollnumber INT NOT NULL,
    icpsr DECIMAL (20,2) NOT NULL,
    cast_code DECIMAL (20,2) NOT NULL,
    prob VARCHAR(255),
    PRIMARY KEY(congress, rollnumber, icpsr)
);

CREATE TABLE Vote_Cast_Code (
    cast_code DECIMAL (20,2) NOT NULL,
    descr VARCHAR(255) NOT NULL,
    PRIMARY KEY(cast_code)
);

CREATE TABLE Candidate_Vote_Data (
    congress INT NOT NULL,
    chamber VARCHAR(255) NOT NULL,
    rollnumber INT NOT NULL,
    vote_date DATE NOT NULL,
    vote_session DECIMAL (20,2),
    clerk_rollnumber DECIMAL (20,2),
    yea_count INT,
    nay_count INT,
    nominate_mid_1 DECIMAL (20,2),
    nominate_mid_2 DECIMAL (20,2),
    nominate_spread_1 DECIMAL (20,2),
    nominate_spread_2 DECIMAL (20,2),
    nominate_log_likelihood DECIMAL (20,2),
    bill_number VARCHAR(225),
    vote_result VARCHAR(225),
    vote_desc VARCHAR(3750),
    vote_question VARCHAR(225),
    dtl_desc VARCHAR(2800),
    PRIMARY KEY(rollnumber, congress)
);

CREATE TABLE Candidate_Members (
    congress INT NOT NULL,
    chamber VARCHAR(255) NOT NULL,
    icpsr DECIMAL (20,2) NOT NULL,
    state_icpsr INT NOT NULL,
    district_code DECIMAL (20,2) NOT NULL,
    state_abbrev VARCHAR(255) NOT NULL,
    party_code INT NOT NULL,
    occupancy INT,
    last_means INT,
    bioname VARCHAR(255) NOT NULL,
    bioguide_id VARCHAR(255),
    born DECIMAL (20,2),
    died DECIMAL (20,2),
    nominate_dim1 DECIMAL (20,2),
    nominate_dim2 DECIMAL (20,2),
    nominate_log_likelihood DECIMAL (20,2),
    nominate_geo_mean_probability DECIMAL (20,2),
    nominate_number_of_votes DECIMAL (20,2),
    nominate_number_of_errors DECIMAL (20,2),
    conditional DECIMAL (20,2),
    nokken_poole_dim1 DECIMAL (20,2),
    nokken_poole_dim2 DECIMAL (20,2),
    PRIMARY KEY(congress, icpsr)
);

CREATE TABLE Candidate_Party_Codes (
    party_code INT NOT NULL,
    party VARCHAR(255) NOT NULL,
    PRIMARY KEY(party_code)
);

CREATE TABLE Senate_Legislation_Topics (
    legislation_number VARCHAR(255) NOT NULL PRIMARY KEY,
    legislation_URL VARCHAR(255) NOT NULL,
    title VARCHAR(1255) NOT NULL,
    sponsor VARCHAR(255) NOT NULL,
    cosponsor1 VARCHAR(255),
    cosponsor2 VARCHAR(255),
    cosponsor3 VARCHAR(255),
    cosponsor4 VARCHAR(255),
    cosponsor5 VARCHAR(255),
    subject1 VARCHAR(255),
    subject2 VARCHAR(255),
    subject3 VARCHAR(255),
    subject4 VARCHAR(255),
    subject5 VARCHAR(255)
);


--implement search bar by category
--search by from and to whichever entity
