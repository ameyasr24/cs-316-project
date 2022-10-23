\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);

\COPY Committees FROM 'Committees.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY States FROM 'States.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.states_id_seq',
                         (SELECT MAX(id)+1 FROM States),
                         false);

\COPY Candidate_Vote FROM 'Voting.csv' WITH DELIMITER ',' NULL '' CSV;

/* \COPY Candidate_Vote_Data FROM 'Candidate_Vote_Data.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Candidate_Member_Votes FROM 'Candidate_Member_Votes.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Candidate_Members FROM 'Candidate_Members.csv' WITH DELIMITER ',' NULL '' CSV; */

