LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/CUP_POINTS.csv' INTO TABLE CUP_POINTS FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS  (
    game_point_id,
    game_player_id,
    game_play_id,
    game_id,
    game,
    round_of_game,
    phase,
    season_player_id,
    season_team_id,
    player,
    action_id,
    action_of_play,
    points,
    coord_x,
    coord_y,
    zone_of_play,
    minute,
    points_a,
    points_b,
    date_time_stp
);

-- End of load table for CUP_POINTS

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/LIG_POINTS.csv' INTO TABLE LIG_POINTS FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (
    game_point_id,
    game_player_id,
    game_play_id,
    game_id,
    game,
    round_of_game,
    phase,
    season_player_id,
    season_team_id,
    player,
    action_id,
    action_of_play,
    points,
    coord_x,
    coord_y,
    zone_of_play,
    minute,
    points_a,
    points_b,
    date_time_stp
);


-- End of load table for LIG_POINTS

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/CUP_TEAMS.csv' INTO TABLE CUP_TEAMS FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (
    season_team_id,
    games_played,
    minutes_played,
    points,
    two_points_made,
    two_points_attempted,
    three_points_made,
    three_points_attempted,
    free_throws_made,
    free_throws_attempted,
    offensive_rebounds,
    defensive_rebounds,
    total_rebounds,
    assists,
    steals,
    turnovers,
    blocks_favour,
    blocks_against,
    fouls_committed,
    fouls_received,
    valuation,
    minutes_per_game,
    points_per_game,
    two_points_made_per_game,
    two_points_attempted_per_game,
    two_points_percentage,
    three_points_made_per_game,
    three_points_attempted_per_game,
    three_points_percentage,
    free_throws_made_per_game,
    free_throws_attempted_per_game,
    free_throws_percentage,
    offensive_rebounds_per_game,
    defensive_rebounds_per_game,
    total_rebounds_per_game,
    assists_per_game,
    steals_per_game,
    turnovers_per_game,
    blocks_favour_per_game,
    blocks_against_per_game,
    fouls_committed_per_game,
    fouls_received_per_game,
    valuation_per_game
);

-- End of load table for CUP_TEAMS

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/LIG_TEAMS.csv' INTO TABLE LIG_TEAMS FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (
    season_team_id,
    games_played,
    minutes_played,
    points,
    two_points_made,
    two_points_attempted,
    three_points_made,
    three_points_attempted,
    free_throws_made,
    free_throws_attempted,
    offensive_rebounds,
    defensive_rebounds,
    total_rebounds,
    assists,
    steals,
    turnovers,
    blocks_favour,
    blocks_against,
    fouls_committed,
    fouls_received,
    valuation,
    minutes_per_game,
    points_per_game,
    two_points_made_per_game,
    two_points_attempted_per_game,
    two_points_percentage,
    three_points_made_per_game,
    three_points_attempted_per_game,
    three_points_percentage,
    free_throws_made_per_game,
    free_throws_attempted_per_game,
    free_throws_percentage,
    offensive_rebounds_per_game,
    defensive_rebounds_per_game,
    total_rebounds_per_game,
    assists_per_game,
    steals_per_game,
    turnovers_per_game,
    blocks_favour_per_game,
    blocks_against_per_game,
    fouls_committed_per_game,
    fouls_received_per_game,
    valuation_per_game
);

-- End of load table for LIG_TEAMS

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/CUP_COMPARISON.csv' INTO TABLE CUP_COMPARISON FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES (
    game_id,
    game,
    round_of_game,
    phase,
    season_team_id_a,
    season_team_id_b,
    fast_break_points_a,
    fast_break_points_b,
    turnover_points_a,
    turnover_points_b,
    second_chance_points_a,
    second_chance_points_b,
    defensive_rebounds_a,
    offensive_rebounds_b,
    offensive_rebounds_a,
    defensive_rebounds_b,
    turnovers_starters_a,
    turnovers_bench_a,
    turnovers_starters_b,
    turnovers_bench_b,
    steals_starters_a,
    steals_bench_a,
    steals_starters_b,
    steals_bench_b,
    assists_starters_a,
    assists_bench_a,
    assists_starters_b,
    assists_bench_b,
    points_starters_a,
    points_bench_a,
    points_starters_b,
    points_bench_b,
    max_lead_a,
    max_lead_b,
    minute_max_lead_a,
    minute_max_lead_b
);

-- End of load table for CUP_COMPARISON

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/LIG_COMPARISON.csv' INTO TABLE LIG_COMPARISON FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES (
    game_id,
    game,
    round_of_game,
    phase,
    season_team_id_a,
    season_team_id_b,
    fast_break_points_a,
    fast_break_points_b,
    turnover_points_a,
    turnover_points_b,
    second_chance_points_a,
    second_chance_points_b,
    defensive_rebounds_a,
    offensive_rebounds_b,
    offensive_rebounds_a,
    defensive_rebounds_b,
    turnovers_starters_a,
    turnovers_bench_a,
    turnovers_starters_b,
    turnovers_bench_b,
    steals_starters_a,
    steals_bench_a,
    steals_starters_b,
    steals_bench_b,
    assists_starters_a,
    assists_bench_a,
    assists_starters_b,
    assists_bench_b,
    points_starters_a,
    points_bench_a,
    points_starters_b,
    points_bench_b,
    max_lead_a,
    max_lead_b,
    minute_max_lead_a,
    minute_max_lead_b
);

-- End of load table for LIG_COMPARISON

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/CUP_HEADER.csv' INTO TABLE CUP_HEADER FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES (
    game_id,
    game,
    date_of_game,
    time_of_game,
    round_of_game,
    phase,
    season_team_id_a,
    season_team_id_b,
    score_a,
    score_b,
    coach_a,
    coach_b,
    game_time,
    referee_1,
    referee_2,
    referee_3,
    stadium,
    capacity,
    fouls_a,
    fouls_b,
    timeouts_a,
    timeouts_b,
    score_quarter_1_a,
    score_quarter_2_a,
    score_quarter_3_a,
    score_quarter_4_a,
    score_quarter_1_b,
    score_quarter_2_b,
    score_quarter_3_b,
    score_quarter_4_b,
    score_extra_time_1_a,
    score_extra_time_2_a,
    score_extra_time_3_a,
    score_extra_time_4_a,
    score_extra_time_1_b,
    score_extra_time_2_b,
    score_extra_time_3_b,
    score_extra_time_4_b,
    winner
);

-- End of load table for CUP_HEADER

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/LIG_HEADER.csv' INTO TABLE LIG_HEADER FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES (
    game_id,
    game,
    date_of_game,
    time_of_game,
    round_of_game,
    phase,
    season_team_id_a,
    season_team_id_b,
    score_a,
    score_b,
    coach_a,
    coach_b,
    game_time,
    referee_1,
    referee_2,
    referee_3,
    stadium,
    capacity,
    fouls_a,
    fouls_b,
    timeouts_a,
    timeouts_b,
    score_quarter_1_a,
    score_quarter_2_a,
    score_quarter_3_a,
    score_quarter_4_a,
    score_quarter_1_b,
    score_quarter_2_b,
    score_quarter_3_b,
    score_quarter_4_b,
    score_extra_time_1_a,
    score_extra_time_2_a,
    score_extra_time_3_a,
    score_extra_time_4_a,
    score_extra_time_1_b,
    score_extra_time_2_b,
    score_extra_time_3_b,
    score_extra_time_4_b,
    winner
);

-- End of load table for LIG_HEADER

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/CUP_PLAY_BY_PLAY.csv' INTO TABLE CUP_PLAY_BY_PLAY FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES (
    game_play_id,
    game_player_id,
    game_point_id,
    game_id,
    game,
    round_of_game,
    phase,
    season_player_id,
    season_team_id,
    quarter,
    play_type,
    player,
    team,
    @dorsal,
    minute,
    @points_a,
    @points_b,
    play_info
);

UPDATE CUP_PLAY_BY_PLAY
SET points_a = NULLIF(@points_a, ''),
    points_b = NULLIF(@points_b, ''),
    dorsal = NULLIF(@dorsal, '');

-- End of load table for CUP_PLAY_BY_PLAY

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/LIG_PLAY_BY_PLAY.csv' INTO TABLE LIG_PLAY_BY_PLAY FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES (
    game_play_id,
    game_player_id,
    game_point_id,
    game_id,
    game,
    round_of_game,
    phase,
    season_player_id,
    season_team_id,
    quarter,
    play_type,
    player,
    team,
    @dorsal,
    minute,
    @points_a,
    @points_b,
    play_info
);

UPDATE LIG_PLAY_BY_PLAY
    SET points_a = NULLIF(@points_a, ''),
        points_b = NULLIF(@points_b, ''),
        dorsal = NULLIF(@dorsal, '');


-- End of load table for LIG_PLAY_BY_PLAY

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/CUP_BOX_SCORE.csv' INTO TABLE CUP_BOX_SCORE FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES (
    game_player_id,
    game_id,
    game,
    round_of_game,
    phase,
    season_player_id,
    season_team_id,
    is_starter,
    is_playing,
    @dorsal,
    player,
    points,
    two_points_made,
    two_points_attempted,
    three_points_made,
    three_points_attempted,
    free_throws_made,
    free_throws_attempted,
    offensive_rebounds,
    defensive_rebounds,
    total_rebounds,
    assists,
    steals,
    turnovers,
    blocks_favour,
    blocks_against,
    fouls_committed,
    fouls_received,
    valuation
);

UPDATE CUP_BOX_SCORE
    SET dorsal = NULLIF(@dorsal, '');

-- End of load table for CUP_BOX_SCORE

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/LIG_BOX_SCORE.csv' INTO TABLE LIG_BOX_SCORE FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES (
    game_player_id,
    game_id,
    game,
    round_of_game,
    phase,
    season_player_id,
    season_team_id,
    is_starter,
    is_playing,
    @dorsal,
    player,
    points,
    two_points_made,
    two_points_attempted,
    three_points_made,
    three_points_attempted,
    free_throws_made,
    free_throws_attempted,
    offensive_rebounds,
    defensive_rebounds,
    total_rebounds,
    assists,
    steals,
    turnovers,
    blocks_favour,
    blocks_against,
    fouls_committed,
    fouls_received,
    valuation
);

UPDATE LIG_BOX_SCORE
    SET dorsal = NULLIF(@dorsal, '');

-- End of load table for LIG_BOX_SCORE

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/CUP_PLAYERS.csv' INTO TABLE CUP_PLAYERS FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES (
    season_player_id,
    season_team_id,
    player,
    games_played,
    games_started,
    minutes_played,
    points,
    two_points_made,
    two_points_attempted,
    three_points_made,
    three_points_attempted,
    free_throws_made,
    free_throws_attempted,
    offensive_rebounds,
    defensive_rebounds,
    total_rebounds,
    assists,
    steals,
    turnovers,
    blocks_favour,
    blocks_against,
    fouls_committed,
    fouls_received,
    valuation,
    minutes_per_game,
    @points_per_game,
    two_points_made_per_game,
    two_points_attempted_per_game,
    two_points_percentage,
    three_points_made_per_game,
    three_points_attempted_per_game,
    three_points_percentage,
    free_throws_made_per_game,
    free_throws_attempted_per_game,
    free_throws_percentage,
    offensive_rebounds_per_game,
    defensive_rebounds_per_game,
    total_rebounds_per_game,
    assists_per_game,
    steals_per_game,
    turnovers_per_game,
    blocks_favour_per_game,
    blocks_against_per_game,
    fouls_committed_per_game,
    fouls_received_per_game,
    valuation_per_game
);

-- End of load table for CUP_PLAYERS

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/LIG_PLAYERS.csv' INTO TABLE LIG_PLAYERS FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES (
    season_player_id,
    season_team_id,
    player,
    games_played,
    games_started,
    minutes_played,
    points,
    two_points_made,
    two_points_attempted,
    three_points_made,
    three_points_attempted,
    free_throws_made,
    free_throws_attempted,
    offensive_rebounds,
    defensive_rebounds,
    total_rebounds,
    assists,
    steals,
    turnovers,
    blocks_favour,
    blocks_against,
    fouls_committed,
    fouls_received,
    valuation,
    minutes_per_game,
    @points_per_game,
    @two_points_made_per_game,
    @two_points_attempted_per_game,
    two_points_percentage,
    three_points_made_per_game,
    three_points_attempted_per_game,
    three_points_percentage,
    free_throws_made_per_game,
    free_throws_attempted_per_game,
    free_throws_percentage,
    offensive_rebounds_per_game,
    defensive_rebounds_per_game,
    total_rebounds_per_game,
    assists_per_game,
    steals_per_game,
    turnovers_per_game,
    blocks_favour_per_game,
    blocks_against_per_game,
    fouls_committed_per_game,
    fouls_received_per_game,
    @valuation_per_game
);
UPDATE LIG_PLAYERS 
    SET points_per_game = NULLIF(@points_per_game, 'inf'),
        two_points_made_per_game =  NULLIF(@two_points_made_per_game, 'inf'),
        two_points_attempted_per_game =  NULLIF(@two_points_attempted_per_game, 'inf'),
        valuation_per_game =  NULLIF(@valuation_per_game, 'inf');

-- End of load table for LIG_PLAYERS

LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/unique_teams_with_logos.csv" INTO TABLE teams FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (
    abbreviation,
    full_name,
    logo_url
);
UPDATE teams
    SET logo_url = NULLIF(logo_url, '');

-- End of load table for teams