create  DATABASE BASKETBALL;

USE BASKETBALL;

-- Step 1: Create tables without foreign keys

CREATE TABLE CUP_POINTS(
    game_point_id VARCHAR(50) PRIMARY KEY,
    game_player_id VARCHAR(50),
    game_play_id VARCHAR(50),
    game_id VARCHAR(50),
    game VARCHAR(50),
    rounds INT,
    phase VARCHAR(50),
    season_player_id VARCHAR(50),
    season_team_id VARCHAR(50),
    player VARCHAR(50),
    action_id VARCHAR(50),
    actions VARCHAR(50),
    points INT,
    coord_x INT,
    coord_y INT,
    zones CHAR(1),
    minute INT,
    points_a INT,
    points_b INT,
    time_stamp DATETIME
);

CREATE TABLE LIG_POINTS(
    game_point_id VARCHAR(50) PRIMARY KEY,
    game_player_id VARCHAR(50),
    game_play_id VARCHAR(50),
    game_id VARCHAR(50),
    game VARCHAR(50),
    rounds INT,
    phase VARCHAR(50),
    season_player_id VARCHAR(50),
    season_team_id VARCHAR(50),
    player VARCHAR(50),
    action_id VARCHAR(50),
    actions VARCHAR(50),
    points INT ,
    coord_x INT,
    coord_y INT,
    zones CHAR(1),
    minute INT ,
    points_a INT ,
    points_b INT ,
    time_stamp DATETIME
);

CREATE TABLE CUP_TEAMS (
    season_team_id VARCHAR(50) PRIMARY KEY,
    games_played INT,
    minutes_played FLOAT,
    points INT,
    two_points_made INT,
    two_points_attempted INT,
    three_points_made INT,
    three_points_attempted INT,
    free_throws_made INT,
    free_throws_attempted INT,
    offensive_rebounds INT,
    defensive_rebounds INT,
    total_rebounds INT,
    assists INT,
    steals INT,
    turnovers INT,
    blocks_favour INT,
    blocks_against INT,
    fouls_committed INT,
    fouls_received INT,
    valuation INT,
    minutes_per_game FLOAT,
    points_per_game FLOAT,
    two_points_made_per_game FLOAT,
    two_points_attempted_per_game FLOAT,
    two_points_percentage FLOAT,
    three_points_made_per_game FLOAT,
    three_points_attempted_per_game FLOAT,
    three_points_percentage FLOAT,
    free_throws_made_per_game FLOAT,
    free_throws_attempted_per_game FLOAT,
    free_throws_percentage FLOAT,
    offensive_rebounds_per_game FLOAT,
    defensive_rebounds_per_game FLOAT,
    total_rebounds_per_game FLOAT,
    assists_per_game FLOAT,
    steals_per_game FLOAT,
    turnovers_per_game FLOAT,
    blocks_favour_per_game FLOAT,
    blocks_against_per_game FLOAT,
    fouls_committed_per_game FLOAT,
    fouls_received_per_game FLOAT,
    valuation_per_game FLOAT
);

CREATE TABLE LIG_TEAMS (
    season_team_id VARCHAR(50) PRIMARY KEY,
    games_played INT,
    minutes_played FLOAT,
    points INT,
    two_points_made INT,
    two_points_attempted INT,
    three_points_made INT,
    three_points_attempted INT,
    free_throws_made INT,
    free_throws_attempted INT,
    offensive_rebounds INT,
    defensive_rebounds INT,
    total_rebounds INT,
    assists INT,
    steals INT,
    turnovers INT,
    blocks_favour INT,
    blocks_against INT,
    fouls_committed INT,
    fouls_received INT,
    valuation INT,
    minutes_per_game FLOAT,
    points_per_game FLOAT,
    two_points_made_per_game FLOAT,
    two_points_attempted_per_game FLOAT,
    two_points_percentage FLOAT,
    three_points_made_per_game FLOAT,
    three_points_attempted_per_game FLOAT,
    three_points_percentage FLOAT,
    free_throws_made_per_game FLOAT,
    free_throws_attempted_per_game FLOAT,
    free_throws_percentage FLOAT,
    offensive_rebounds_per_game FLOAT,
    defensive_rebounds_per_game FLOAT,
    total_rebounds_per_game FLOAT,
    assists_per_game FLOAT,
    steals_per_game FLOAT,
    turnovers_per_game FLOAT,
    blocks_favour_per_game FLOAT,
    blocks_against_per_game FLOAT,
    fouls_committed_per_game FLOAT,
    fouls_received_per_game FLOAT,
    valuation_per_game FLOAT
);

CREATE TABLE CUP_COMPARISON(
    game_id VARCHAR(50) PRIMARY KEY,
    game VARCHAR(50),
    rounds INT,
    phase VARCHAR(50),
    season_team_id_a VARCHAR(50),
    season_team_id_b VARCHAR(50),
    fast_break_points_a INT,
    fast_break_points_b INT,
    turnover_points_a INT,
    turnover_points_b INT,
    second_chance_points_a INT,
    second_chance_points_b INT,
    defensive_rebounds_a INT,
    defensive_rebounds_b INT,
    turnovers_starters_a INT,
    turnovers_bench_a INT,
    turnovers_starters_b INT,
    turnovers_bench_b INT,
    steals_starters_a INT,
    steals_bench_a INT,
    steals_starters_b INT,
    steals_bench_b INT,
    assists_starters_a INT,
    assists_bench_a INT,
    assists_starters_b INT,
    assists_bench_b INT,
    points_starters_a INT,
    points_bench_a INT,
    points_starters_b INT,
    points_bench_b INT,
    max_lead_a INT,
    max_lead_b INT,
    minute_max_lead_a INT,
    minute_max_lead_b INT,
    points_max_lead_a VARCHAR(50),
    points_max_lead_b VARCHAR(50)
);

-- Creating LIG_COMPARISON table without foreign keys
CREATE TABLE LIG_COMPARISON(
    game_id VARCHAR(50) PRIMARY KEY,
    game VARCHAR(50),
    rounds INT,
    phase VARCHAR(50),
    season_team_id_a VARCHAR(50),
    season_team_id_b VARCHAR(50),
    fast_break_points_a INT,
    fast_break_points_b INT,
    turnover_points_a INT,
    turnover_points_b INT,
    second_chance_points_a INT,
    second_chance_points_b INT,
    defensive_rebounds_a INT,
    defensive_rebounds_b INT,
    turnovers_starters_a INT,
    turnovers_bench_a INT,
    turnovers_starters_b INT,
    turnovers_bench_b INT,
    steals_starters_a INT,
    steals_bench_a INT,
    steals_starters_b INT,
    steals_bench_b INT,
    assists_starters_a INT,
    assists_bench_a INT,
    assists_starters_b INT,
    assists_bench_b INT,
    points_starters_a INT,
    points_bench_a INT,
    points_starters_b INT,
    points_bench_b INT,
    max_lead_a INT,
    max_lead_b INT,
    minute_max_lead_a INT,
    minute_max_lead_b INT,
    points_max_lead_a VARCHAR(50),
    points_max_lead_b VARCHAR(50)
);

-- Creating CUP_HEADER table without foreign keys
CREATE TABLE CUP_HEADER(
    game_id VARCHAR(50) PRIMARY KEY,
    game VARCHAR(50),
    dates DATE,
    timess TIME,
    rounds INT,
    phase VARCHAR(50),
    season_team_id_a VARCHAR(50),
    season_team_id_b VARCHAR(50),
    score_a INT,
    score_b INT,
    team_a VARCHAR(50),
    team_b VARCHAR(50),
    coach_a VARCHAR(50),
    coach_b VARCHAR(50),
    game_time TIME,
    referee_1 VARCHAR(50),
    referee_2 VARCHAR(50),
    referee_3 VARCHAR(50),
    stadium VARCHAR(50),
    capacity INT,
    fouls_a INT,
    fouls_b INT,
    timeouts_a INT,
    timeouts_b INT,
    score_quarter_1_a INT,
    score_quarter_2_a INT,
    score_quarter_3_a INT,
    score_quarter_4_a INT,
    score_quarter_1_b INT,
    score_quarter_2_b INT,
    score_quarter_3_b INT,
    score_quarter_4_b INT,
    score_extra_time_1_a INT,
    score_extra_time_2_a INT,
    score_extra_time_3_a INT,
    score_extra_time_4_a INT,
    score_extra_time_1_b INT,
    score_extra_time_2_b INT,
    score_extra_time_3_b INT,
    score_extra_time_4_b INT,
    won CHAR(6)
);

-- Creating LIG_HEADER table without foreign keys
CREATE TABLE LIG_HEADER(
    game_id VARCHAR(50) PRIMARY KEY,
    game VARCHAR(50),
    dates DATE,
    timess TIME,
    rounds INT,
    phase VARCHAR(50),
    season_team_id_a VARCHAR(50),
    season_team_id_b VARCHAR(50),
    score_a INT,
    score_b INT,
    team_a VARCHAR(50),
    team_b VARCHAR(50),
    coach_a VARCHAR(50),
    coach_b VARCHAR(50),
    game_time TIME,
    referee_1 VARCHAR(50),
    referee_2 VARCHAR(50),
    referee_3 VARCHAR(50),
    stadium VARCHAR(50),
    capacity INT,
    fouls_a INT,
    fouls_b INT,
    timeouts_a INT,
    timeouts_b INT,
    score_quarter_1_a INT,
    score_quarter_2_a INT,
    score_quarter_3_a INT,
    score_quarter_4_a INT,
    score_quarter_1_b INT,
    score_quarter_2_b INT,
    score_quarter_3_b INT,
    score_quarter_4_b INT,
    score_extra_time_1_a INT,
    score_extra_time_2_a INT,
    score_extra_time_3_a INT,
    score_extra_time_4_a INT,
    score_extra_time_1_b INT,
    score_extra_time_2_b INT,
    score_extra_time_3_b INT,
    score_extra_time_4_b INT,
    won CHAR(6)
);

-- Creating CUP_PLAY_BY_PLAY table without foreign keys
CREATE TABLE CUP_PLAY_BY_PLAY(
    game_play_id VARCHAR(50) PRIMARY KEY,
    game_id VARCHAR(50),
    game VARCHAR(50),
    rounds INT,
    phase VARCHAR(50),
    season_code VARCHAR(50),
    quarter VARCHAR(10),
    types INT,
    number_of_play INT,
    team_id VARCHAR(50),
    player_id VARCHAR(50),
    play_type VARCHAR(10),
    player VARCHAR(100),
    team VARCHAR(50),
    dorsal INT,
    minute INT,
    marker_time VARCHAR(10),
    points_a INT,
    points_b INT,
    comment TEXT,
    play_info VARCHAR(100)
);

-- Creating LIG_PLAY_BY_PLAY table without foreign keys
CREATE TABLE LIG_PLAY_BY_PLAY(
    game_play_id VARCHAR(50) PRIMARY KEY,
    game_id VARCHAR(50),
    game VARCHAR(50),
    rounds INT,
    phase VARCHAR(50),
    season_code VARCHAR(50),
    quarter VARCHAR(10),
    types INT,
    number_of_play INT,
    team_id VARCHAR(50),
    player_id VARCHAR(50),
    play_type VARCHAR(10),
    player VARCHAR(100),
    team VARCHAR(50),
    dorsal INT,
    minute INT,
    marker_time VARCHAR(10),
    points_a INT,
    points_b INT,
    comment TEXT,
    play_info VARCHAR(100)
);

-- Creating CUP_BOX_SCORE table without foreign keys
CREATE TABLE CUP_BOX_SCORE(
    game_player_id VARCHAR(50) PRIMARY KEY,
    game_play_id VARCHAR(50),
    game_id VARCHAR(50),
    game VARCHAR(50),
    rounds INT,
    phase VARCHAR(50),
    season_player_id VARCHAR(50),
    season_team_id VARCHAR(50),
    player_id VARCHAR(50),
    is_starter BOOLEAN,
    is_playing BOOLEAN,
    team_id VARCHAR(50),
    dorsal INT,
    player VARCHAR(100),
    minutes_played TIME,
    points INT,
    two_points_made INT,
    two_points_attempted INT,
    three_points_made INT,
    three_points_attempted INT,
    free_throws_made INT,
    free_throws_attempted INT,
    offensive_rebounds INT,
    defensive_rebounds INT,
    total_rebounds INT,
    assists INT,
    steals INT,
    turnovers INT,
    blocks_favour INT,
    blocks_against INT,
    fouls_committed INT,
    fouls_received INT,
    valuation INT,
    plus_minus INT
);

-- Creating LIG_BOX_SCORE table without foreign keys
CREATE TABLE LIG_BOX_SCORE(
    game_player_id VARCHAR(50) PRIMARY KEY,
    game_id VARCHAR(50),
    game VARCHAR(50),
    rounds INT,
    phase VARCHAR(50),
    season_code VARCHAR(50),
    player_id VARCHAR(50),
    is_starter BOOLEAN,
    is_playing BOOLEAN,
    team_id VARCHAR(50),
    dorsal INT,
    player VARCHAR(100),
    minutes_played TIME,
    points INT,
    two_points_made INT,
    two_points_attempted INT,
    three_points_made INT,
    three_points_attempted INT,
    free_throws_made INT,
    free_throws_attempted INT,
    offensive_rebounds INT,
    defensive_rebounds INT,
    total_rebounds INT,
    assists INT,
    steals INT,
    turnovers INT,
    blocks_favour INT,
    blocks_against INT,
    fouls_committed INT,
    fouls_received INT,
    valuation INT,
    plus_minus INT
);

-- Creating CUP_PLAYERS table without foreign keys
CREATE TABLE CUP_PLAYERS(
    season_player_id VARCHAR(50) PRIMARY KEY,
    season_team_id VARCHAR(50),
    player VARCHAR(100),
    games_played INT,
    games_started INT,
    minutes_played FLOAT,
    points INT,
    two_points_made INT,
    two_points_attempted INT,
    three_points_made INT,
    three_points_attempted INT,
    free_throws_made INT,
    free_throws_attempted INT,
    offensive_rebounds INT,
    defensive_rebounds INT,
    total_rebounds INT,
    assists INT,
    steals INT,
    turnovers INT,
    blocks_favour INT,
    blocks_against INT,
    fouls_committed INT,
    fouls_received INT,
    valuation INT,
    minutes_per_game FLOAT,
    points_per_game FLOAT,
    two_points_made_per_game FLOAT,
    two_points_attempted_per_game FLOAT,
    two_points_percentage FLOAT,
    three_points_made_per_game FLOAT,
    three_points_attempted_per_game FLOAT,
    three_points_percentage FLOAT,
    free_throws_made_per_game FLOAT,
    free_throws_attempted_per_game FLOAT,
    free_throws_percentage FLOAT,
    offensive_rebounds_per_game FLOAT,
    defensive_rebounds_per_game FLOAT,
    total_rebounds_per_game FLOAT,
    assists_per_game FLOAT,
    steals_per_game FLOAT,
    turnovers_per_game FLOAT,
    blocks_favour_per_game FLOAT,
    blocks_against_per_game FLOAT,
    fouls_committed_per_game FLOAT,
    fouls_received_per_game FLOAT,
    valuation_per_game FLOAT
);

-- Creating LIG_PLAYERS table without foreign keys
CREATE TABLE LIG_PLAYERS(
    season_player_id VARCHAR(50) PRIMARY KEY,
    season_team_id VARCHAR(50),
    player VARCHAR(100),
    games_played INT,
    games_started INT,
    minutes_played FLOAT,
    points INT,
    two_points_made INT,
    two_points_attempted INT,
    three_points_made INT,
    three_points_attempted INT,
    free_throws_made INT,
    free_throws_attempted INT,
    offensive_rebounds INT,
    defensive_rebounds INT,
    total_rebounds INT,
    assists INT,
    steals INT,
    turnovers INT,
    blocks_favour INT,
    blocks_against INT,
    fouls_committed INT,
    fouls_received INT,
    valuation INT,
    minutes_per_game FLOAT,
    points_per_game FLOAT,
    two_points_made_per_game FLOAT,
    two_points_attempted_per_game FLOAT,
    two_points_percentage FLOAT,
    three_points_made_per_game FLOAT,
    three_points_attempted_per_game FLOAT,
    three_points_percentage FLOAT,
    free_throws_made_per_game FLOAT,
    free_throws_attempted_per_game FLOAT,
    free_throws_percentage FLOAT,
    offensive_rebounds_per_game FLOAT,
    defensive_rebounds_per_game FLOAT,
    total_rebounds_per_game FLOAT,
    assists_per_game FLOAT,
    steals_per_game FLOAT,
    turnovers_per_game FLOAT,
    blocks_favour_per_game FLOAT,
    blocks_against_per_game FLOAT,
    fouls_committed_per_game FLOAT,
    fouls_received_per_game FLOAT,
    valuation_per_game FLOAT
);


-- Step 2: Add Foreign Keys

-- Adding Foreign Keys for CUP_POINTS table
ALTER TABLE CUP_POINTS
    ADD CONSTRAINT fk_game_player_id FOREIGN KEY (game_player_id) REFERENCES CUP_BOX_SCORE(game_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_POINTS
    ADD CONSTRAINT fk_game_play_id FOREIGN KEY (game_play_id) REFERENCES CUP_PLAY_BY_PLAY(game_play_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_POINTS
    ADD CONSTRAINT fk_game_id FOREIGN KEY (game_id) REFERENCES CUP_COMPARISON(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_POINTS
    ADD CONSTRAINT fk_season_player_id FOREIGN KEY (season_player_id) REFERENCES CUP_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_POINTS
    ADD CONSTRAINT fk_season_team_id FOREIGN KEY (season_team_id) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_POINTS table
ALTER TABLE LIG_POINTS
    ADD CONSTRAINT fk_game_player_id_lig FOREIGN KEY (game_player_id) REFERENCES LIG_BOX_SCORE(game_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_POINTS
    ADD CONSTRAINT fk_game_play_id_lig FOREIGN KEY (game_play_id) REFERENCES LIG_PLAY_BY_PLAY(game_play_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_POINTS
    ADD CONSTRAINT fk_game_id_lig FOREIGN KEY (game_id) REFERENCES LIG_COMPARISON(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_POINTS
    ADD CONSTRAINT fk_season_player_id_lig FOREIGN KEY (season_player_id) REFERENCES LIG_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_POINTS
    ADD CONSTRAINT fk_season_team_id_lig FOREIGN KEY (season_team_id) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for CUP_COMPARISON table
ALTER TABLE CUP_COMPARISON
    ADD CONSTRAINT fk_game_id_header FOREIGN KEY (game_id) REFERENCES CUP_HEADER(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_COMPARISON
    ADD CONSTRAINT fk_game_id_points FOREIGN KEY (game_id) REFERENCES CUP_POINTS(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_COMPARISON
    ADD CONSTRAINT fk_season_team_id_a FOREIGN KEY (season_team_id_a) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_COMPARISON
    ADD CONSTRAINT fk_season_team_id_b FOREIGN KEY (season_team_id_b) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_COMPARISON table
ALTER TABLE LIG_COMPARISON
    ADD CONSTRAINT fk_game_id_header_lig FOREIGN KEY (game_id) REFERENCES LIG_HEADER(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_COMPARISON
    ADD CONSTRAINT fk_game_id_points_lig FOREIGN KEY (game_id) REFERENCES LIG_POINTS(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_COMPARISON
    ADD CONSTRAINT fk_season_team_id_a_lig FOREIGN KEY (season_team_id_a) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_COMPARISON
    ADD CONSTRAINT fk_season_team_id_b_lig FOREIGN KEY (season_team_id_b) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for CUP_HEADER table
ALTER TABLE CUP_HEADER
    ADD CONSTRAINT fk_game_id_comparison FOREIGN KEY (game_id) REFERENCES CUP_COMPARISON(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_HEADER
    ADD CONSTRAINT fk_game_id_points_header FOREIGN KEY (game_id) REFERENCES CUP_POINTS(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_HEADER
    ADD CONSTRAINT fk_season_team_id_a_header FOREIGN KEY (season_team_id_a) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_HEADER
    ADD CONSTRAINT fk_season_team_id_b_header FOREIGN KEY (season_team_id_b) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_HEADER table
ALTER TABLE LIG_HEADER
    ADD CONSTRAINT fk_game_id_comparison_lig FOREIGN KEY (game_id) REFERENCES LIG_COMPARISON(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_HEADER
    ADD CONSTRAINT fk_game_id_points_header_lig FOREIGN KEY (game_id) REFERENCES LIG_POINTS(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_HEADER
    ADD CONSTRAINT fk_season_team_id_a_header_lig FOREIGN KEY (season_team_id_a) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_HEADER
    ADD CONSTRAINT fk_season_team_id_b_header_lig FOREIGN KEY (season_team_id_b) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for CUP_PLAY_BY_PLAY table
ALTER TABLE CUP_PLAY_BY_PLAY
    ADD CONSTRAINT fk_game_id_comparison FOREIGN KEY (game_id) REFERENCES CUP_COMPARISON(game_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_PLAY_BY_PLAY table
ALTER TABLE LIG_PLAY_BY_PLAY
    ADD CONSTRAINT fk_game_id_comparison_lig FOREIGN KEY (game_id) REFERENCES LIG_COMPARISON(game_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for CUP_BOX_SCORE table
ALTER TABLE CUP_BOX_SCORE
    ADD CONSTRAINT fk_game_id_box FOREIGN KEY (game_id) REFERENCES CUP_COMPARISON(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_BOX_SCORE
    ADD CONSTRAINT fk_game_play_id_box FOREIGN KEY (game_play_id) REFERENCES CUP_PLAY_BY_PLAY(game_play_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_BOX_SCORE
    ADD CONSTRAINT fk_season_player_id_box FOREIGN KEY (season_player_id) REFERENCES CUP_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_BOX_SCORE
    ADD CONSTRAINT fk_season_team_id_box FOREIGN KEY (season_team_id) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_BOX_SCORE table
ALTER TABLE LIG_BOX_SCORE
    ADD CONSTRAINT fk_game_id_box_lig FOREIGN KEY (game_id) REFERENCES LIG_COMPARISON(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_BOX_SCORE
    ADD CONSTRAINT fk_game_play_id_box_lig FOREIGN KEY (game_play_id) REFERENCES LIG_PLAY_BY_PLAY(game_play_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_BOX_SCORE
    ADD CONSTRAINT fk_season_player_id_box_lig FOREIGN KEY (season_player_id) REFERENCES LIG_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_BOX_SCORE
    ADD CONSTRAINT fk_season_team_id_box_lig FOREIGN KEY (season_team_id) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for CUP_PLAYERS table
ALTER TABLE CUP_PLAYERS
    ADD CONSTRAINT fk_season_team_id FOREIGN KEY (season_team_id) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_PLAYERS table
ALTER TABLE LIG_PLAYERS
    ADD CONSTRAINT fk_season_team_id_lig FOREIGN KEY (season_team_id) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;