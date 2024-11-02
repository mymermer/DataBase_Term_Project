create database BASKETBALL;

use BASKETBALL;

CREATE TABLE CUP_POINTS(

    game_point_id VARCHAR(50)	PRIMARY KEY  ,
    game_player_id VARCHAR(50) ,
    game_play_id VARCHAR(50) ,
    game_id VARCHAR(50) ,
    game VARCHAR(50)  ,
    round  INT ,
    phase  VARCHAR(50),
    season_player_id  VARCHAR(50),
    season_team_id  VARCHAR(50),
    player  VARCHAR(50),
    action_id  VARCHAR(50),
    action  VARCHAR(50),
    points  INT,
    coord_x  INT,
    coord_y  INT,
    zone  ENUM("A", "B","C","D","E","F","G","H","I","J"),
    minute INT  ,
    points_a  INT ,
    points_b  INT ,
    timestamp DATETIME, -- need to convert from current time format

    FOREIGN KEY (game_player_id) REFERENCES  CUP_BOX_SCORE(game_player_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (game_play_id) REFERENCES  CUP_PLAY_BY_PLAY(game_play_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (game_id) REFERENCES  CUP_COMPARISON(game_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (season_player_id) REFERENCES  CUP_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (season_team_id) REFERENCES  CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE

);


CREATE TABLE LIG_POINTS(

    game_point_id VARCHAR(50)	PRIMARY KEY  ,
    game_player_id VARCHAR(50) ,
    game_play_id VARCHAR(50) ,
    game_id VARCHAR(50) ,
    game VARCHAR(50)  ,
    round  INT UNSIGNED,
    phase  VARCHAR(50),
    season_player_id  VARCHAR(50),
    season_team_id  VARCHAR(50),
    player  VARCHAR(50),
    action_id  VARCHAR(50),
    action  VARCHAR(50),
    points  INT UNSIGNED,
    coord_x  INT,
    coord_y  INT,
    zone  ENUM("A", "B","C","D","E","F","G","H","I","J"),
    minute INT UNSIGNED ,
    points_a  INT UNSIGNED,
    points_b  INT UNSIGNED,
    timestamp DATETIME, -- need to convert from current time format

    FOREIGN KEY (game_player_id) REFERENCES  LIG_BOX_SCORE(game_player_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (game_play_id) REFERENCES  LIG_PLAY_BY_PLAY(game_play_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (game_id) REFERENCES  LIG_COMPARISON(game_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (season_player_id) REFERENCES  LIG_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (season_team_id) REFERENCES  LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE

);



CREATE TABLE CUP_TEAMS (
    season_team_id VARCHAR(50) PRIMARY KEY,
    games_played INT,
    minutes FLOAT,
	points INT,	
    two_points_made	INT,
    two_points_attempted	INT,
    three_points_made	INT,
    three_points_attempted	INT,
    free_throws_made	INT,
    free_throws_attempted	INT,
    offensive_rebounds	INT,
    defensive_rebounds	INT,
    total_rebounds	INT,
    assists	INT,
    steals	INT,
    turnovers	INT,
    blocks_favour	INT,
    blocks_against	INT,
    fouls_committed	INT,
    fouls_received	INT,
    valuation	INT,
    minutes_per_game	FLOAT,
    points_per_game	FLOAT,
    two_points_made_per_game	FLOAT,
    two_points_attempted_per_game	FLOAT,
    two_points_percentage	FLOAT,
    three_points_made_per_game	FLOAT,
    three_points_attempted_per_game	FLOAT,
    three_points_percentage	FLOAT,
    free_throws_made_per_game	FLOAT,
    free_throws_attempted_per_game	FLOAT,
    free_throws_percentage	FLOAT,
    offensive_rebounds_per_game	FLOAT,
    defensive_rebounds_per_game	FLOAT,
    total_rebounds_per_game	FLOAT,
    assists_per_game	FLOAT,
    steals_per_game	FLOAT,
    turnovers_per_game	FLOAT,
    blocks_favour_per_game	FLOAT,
    blocks_against_per_game	FLOAT,
    fouls_committed_per_game	FLOAT,
    fouls_received_per_game FLOAT,
    valuation_per_game FLOAT
-- NO FOREIGN KEYS IN TEAM TABEL
-- I DID NOT WANT TO FORCE ANY DEFAULT VALUE FOR EMPTY SPACES
);


CREATE TABLE LIG_TEAMS (
    season_team_id VARCHAR(50) PRIMARY KEY,
    games_played INT,
    minutes FLOAT,
	points INT,	
    two_points_made	INT,
    two_points_attempted	INT,
    three_points_made	INT,
    three_points_attempted	INT,
    free_throws_made	INT,
    free_throws_attempted	INT,
    offensive_rebounds	INT,
    defensive_rebounds	INT,
    total_rebounds	INT,
    assists	INT,
    steals	INT,
    turnovers	INT,
    blocks_favour	INT,
    blocks_against	INT,
    fouls_committed	INT,
    fouls_received	INT,
    valuation	INT,
    minutes_per_game	FLOAT,
    points_per_game	FLOAT,
    two_points_made_per_game	FLOAT,
    two_points_attempted_per_game	FLOAT,
    two_points_percentage	FLOAT,
    three_points_made_per_game	FLOAT,
    three_points_attempted_per_game	FLOAT,
    three_points_percentage	FLOAT,
    free_throws_made_per_game	FLOAT,
    free_throws_attempted_per_game	FLOAT,
    free_throws_percentage	FLOAT,
    offensive_rebounds_per_game	FLOAT,
    defensive_rebounds_per_game	FLOAT,
    total_rebounds_per_game	FLOAT,
    assists_per_game	FLOAT,
    steals_per_game	FLOAT,
    turnovers_per_game	FLOAT,
    blocks_favour_per_game	FLOAT,
    blocks_against_per_game	FLOAT,
    fouls_committed_per_game	FLOAT,
    fouls_received_per_game FLOAT,
    valuation_per_game FLOAT
-- NO FOREIGN KEYS IN TEAM TABEL
-- I DID NOT WANT TO FORCE ANY DEFAULT VALUE FOR EMPTY SPACES
);
