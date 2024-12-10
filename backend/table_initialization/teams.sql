-- Create the table
CREATE TABLE teams (
    abbreviation VARCHAR(3),
    full_name VARCHAR(50),
    logo_url VARCHAR(100)
);

-- Load the CSV file into the table
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/unique_teams_with_logos.csv"
INTO TABLE teams
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES -- Skip the header row
(abbreviation, full_name, logo_url)
SET
    logo_url = NULLIF(logo_url, '');
