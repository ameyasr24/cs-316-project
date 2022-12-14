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
\COPY Committee FROM 'updatedcomm.csv' WITH DELIMITER ',' NULL '' CSV ;

\COPY Issues FROM 'Issues.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY States FROM 'States.csv' WITH DELIMITER ',' NULL '' CSV;

SELECT pg_catalog.setval('public.states_id_seq',
                         (SELECT MAX(id)+1 FROM States),
                         false);
                         
\COPY Correlation FROM 'real_correlation_data.csv' (format csv, null "NULL", DELIMITER ',', HEADER);


\COPY Candidate_Member_Votes FROM 'Candidate_Member_Votes.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Vote_Cast_Code FROM 'Vote_Cast_Codes.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Candidate_Vote_Data FROM 'Candidate_Vote_Data.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Candidate_Members FROM 'Candidate_Members.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Candidate_Party_Codes FROM 'Candidate_Party_Codes.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Senate_Legislation_Topics FROM '21-22-senate-voted-bill.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Senate_Results FROM '1976-2020-senate.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Receipts FROM 'Receipts.csv' WITH DELIMITER '|' NULL '' CSV;

\COPY Donations_By_Industry FROM 'donations_industry.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Candidate_Donations FROM 'Candidate_Donations.csv' WITH DELIMITER ',' NULL '' CSV;

