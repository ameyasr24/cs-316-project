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

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Committees (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    from_entity VARCHAR(255) NOT NULL,
    to_entity VARCHAR(255) NOT NULL,
    donation_amount DECIMAL(20,2) NOT NULL,
    from_category VARCHAR(255), -- CHECK (from_category="PAC" ),
    to_category VARCHAR (255) -- CHECK (to_category="candidate")
); 

CREATE TABLE States (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    state_id VARCHAR(255) NOT NULL,
    year INTEGER NOT NULL,
    candidate_name VARCHAR(255) NOT NULL,
    party VARCHAR(255) NOT NULL,
    incumbent_status VARCHAR(255) NOT NULL,
    total_receipts DECIMAL(20,2) NOT NULL,
    percent_vote DECIMAL (20,2) NOT NULL
); 

--implement search bar by category
--search by from and to whichever entity