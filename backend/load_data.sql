LOAD DATA INFILE './dataset/eurocup_teams.csv'
INTO TABLE CUP_TEAMS
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    season_team_id,
    games_played ,
    minutes ,
	points ,	
    two_points_made	,
    two_points_attempted	,
    three_points_made	,
    three_points_attempted	,
    free_throws_made	,
    free_throws_attempted	,
    offensive_rebounds	,
    defensive_rebounds	,
    total_rebounds	,
    assists	,
    steals	,
    turnovers	,
    blocks_favour	,
    blocks_against	,
    fouls_committed	,
    fouls_received	,
    valuation	,
    minutes_per_game	,
    points_per_game	,
    two_points_made_per_game	,
    two_points_attempted_per_game	,
    two_points_percentage	,
    three_points_made_per_game	,
    three_points_attempted_per_game	,
    three_points_percentage	,
    free_throws_made_per_game	,
    free_throws_attempted_per_game	,
    free_throws_percentage	,
    offensive_rebounds_per_game	,
    defensive_rebounds_per_game	,
    total_rebounds_per_game	,
    assists_per_game	,
    steals_per_game	,
    turnovers_per_game	,
    blocks_favour_per_game	,
    blocks_against_per_game	,
    fouls_committed_per_game	,
    fouls_received_per_game ,
    valuation_per_game 

);


LOAD DATA INFILE './dataset/eurocup_points.csv'
INTO TABLE CUP_POINTS
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    game_point_id,
    game_player_id,
    game_play_id,
    game_id,
    game,
    round,
    phase,
    season_player_id,
    season_team_id,
    player,
    action_id,
    action,
    points,
    coord_x,
    coord_y,
    zone,
    minute,
    points_a,
    points_b,
    @timestamp_var -- Temporarily store the timestamp string
)
SET timestamp = STR_TO_DATE(@timestamp_var, '%m/%d/%Y %H:%i'); -- convert time format



LOAD DATA INFILE './dataset/euroleague_teams.csv'
INTO TABLE LIG_TEAMS
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
       season_team_id,
    games_played ,
    minutes ,
	points ,	
    two_points_made	,
    two_points_attempted	,
    three_points_made	,
    three_points_attempted	,
    free_throws_made	,
    free_throws_attempted	,
    offensive_rebounds	,
    defensive_rebounds	,
    total_rebounds	,
    assists	,
    steals	,
    turnovers	,
    blocks_favour	,
    blocks_against	,
    fouls_committed	,
    fouls_received	,
    valuation	,
    minutes_per_game	,
    points_per_game	,
    two_points_made_per_game	,
    two_points_attempted_per_game	,
    two_points_percentage	,
    three_points_made_per_game	,
    three_points_attempted_per_game	,
    three_points_percentage	,
    free_throws_made_per_game	,
    free_throws_attempted_per_game	,
    free_throws_percentage	,
    offensive_rebounds_per_game	,
    defensive_rebounds_per_game	,
    total_rebounds_per_game	,
    assists_per_game	,
    steals_per_game	,
    turnovers_per_game	,
    blocks_favour_per_game	,
    blocks_against_per_game	,
    fouls_committed_per_game	,
    fouls_received_per_game ,
    valuation_per_game 

);


LOAD DATA INFILE './dataset/euroleague_points.csv'
INTO TABLE LIG_POINTS
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    game_point_id,
    game_player_id,
    game_play_id,
    game_id,
    game,
    round,
    phase,
    season_player_id,
    season_team_id,
    player,
    action_id,
    action,
    points,
    coord_x,
    coord_y,
    zone,
    minute,
    points_a,
    points_b,
    @timestamp_var -- Temporarily store the timestamp string
)
SET timestamp = STR_TO_DATE(@timestamp_var, '%m/%d/%Y %H:%i');