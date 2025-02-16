-- Step 2: Add Foreign Keys

-- Adding Foreign Keys for CUP_POINTS table
ALTER TABLE CUP_POINTS
    ADD CONSTRAINT fk_cup_points_teams FOREIGN KEY (season_team_id) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_POINTS
    ADD CONSTRAINT fk_cup_points_header FOREIGN KEY (game_id) REFERENCES CUP_HEADER(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_POINTS
    ADD CONSTRAINT fk_cup_points_play_by_play FOREIGN KEY (game_play_id) REFERENCES CUP_PLAY_BY_PLAY(game_play_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_POINTS
    ADD CONSTRAINT fk_cup_points_box_score FOREIGN KEY (game_player_id) REFERENCES CUP_BOX_SCORE(game_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_POINTS
    ADD CONSTRAINT fk_cup_points_players FOREIGN KEY (season_player_id) REFERENCES CUP_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_POINTS table
ALTER TABLE LIG_POINTS
    ADD CONSTRAINT fk_lig_points_teams FOREIGN KEY (season_team_id) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_POINTS
    ADD CONSTRAINT fk_lig_points_header FOREIGN KEY (game_id) REFERENCES LIG_HEADER(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_POINTS
    ADD CONSTRAINT fk_lig_points_play_by_play FOREIGN KEY (game_play_id) REFERENCES LIG_PLAY_BY_PLAY(game_play_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_POINTS
    ADD CONSTRAINT fk_lig_points_box_score FOREIGN KEY (game_player_id) REFERENCES LIG_BOX_SCORE(game_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_POINTS
    ADD CONSTRAINT fk_lig_points_players FOREIGN KEY (season_player_id) REFERENCES LIG_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for CUP_Teams table
-- ALTER TABLE CUP_TEAMS --None

-- Adding Foreign Keys for LIG_Teams table
-- ALTER TABLE LIG_TEAMS --None
     
-- Adding Foreign Keys for CUP_COMPARISON table
ALTER TABLE CUP_COMPARISON
    ADD CONSTRAINT fk_cup_comparison_header FOREIGN KEY (game_id) REFERENCES CUP_HEADER(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_COMPARISON
    ADD CONSTRAINT fk_cup_comparison_teams_a FOREIGN KEY (season_team_id_a) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_COMPARISON
    ADD CONSTRAINT fk_cup_comparison_teams_b FOREIGN KEY (season_team_id_b) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_COMPARISON table
ALTER TABLE LIG_COMPARISON
    ADD CONSTRAINT fk_lig_comparison_header FOREIGN KEY (game_id) REFERENCES LIG_HEADER(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_COMPARISON
    ADD CONSTRAINT fk_lig_comparison_teams_a FOREIGN KEY (season_team_id_a) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_COMPARISON
    ADD CONSTRAINT fk_lig_comparison_teams_b FOREIGN KEY (season_team_id_b) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for CUP_HEADER table
ALTER TABLE CUP_HEADER
    ADD CONSTRAINT fk_cup_header_teams_a FOREIGN KEY (season_team_id_a) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_HEADER
    ADD CONSTRAINT fk_cup_header_teams_b FOREIGN KEY (season_team_id_b) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_HEADER table
ALTER TABLE LIG_HEADER
    ADD CONSTRAINT fk_lig_header_teams_a FOREIGN KEY (season_team_id_a) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_HEADER
    ADD CONSTRAINT fk_lig_header_teams_b FOREIGN KEY (season_team_id_b) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for CUP_PLAY_BY_PLAY table
ALTER TABLE CUP_PLAY_BY_PLAY
    ADD CONSTRAINT fk_cup_play_by_play_header FOREIGN KEY (game_id) REFERENCES  CUP_HEADER(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_PLAY_BY_PLAY
    ADD CONSTRAINT fk_cup_play_by_play_teams FOREIGN KEY (season_team_id) REFERENCES  CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_PLAY_BY_PLAY
    ADD CONSTRAINT fk_cup_play_by_play_box_score FOREIGN KEY (game_player_id) REFERENCES  CUP_BOX_SCORE(game_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_PLAY_BY_PLAY
    ADD CONSTRAINT fk_cup_play_by_play_players FOREIGN KEY (season_player_id) REFERENCES  CUP_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_PLAY_BY_PLAY
    ADD CONSTRAINT fk_cup_play_by_play_points FOREIGN KEY (game_point_id) REFERENCES  CUP_POINTS(game_point_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_PLAY_BY_PLAY table
ALTER TABLE LIG_PLAY_BY_PLAY
    ADD CONSTRAINT fk_lig_play_by_play_header FOREIGN KEY (game_id) REFERENCES  LIG_HEADER(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_PLAY_BY_PLAY
    ADD CONSTRAINT fk_lig_play_by_play_teams FOREIGN KEY (season_team_id) REFERENCES  LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_PLAY_BY_PLAY
    ADD CONSTRAINT fk_lig_play_by_play_box_score FOREIGN KEY (game_player_id) REFERENCES  LIG_BOX_SCORE(game_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_PLAY_BY_PLAY
    ADD CONSTRAINT fk_lig_play_by_play_players FOREIGN KEY (season_player_id) REFERENCES  LIG_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_PLAY_BY_PLAY
    ADD CONSTRAINT fk_lig_play_by_play_points FOREIGN KEY (game_point_id) REFERENCES  LIG_POINTS(game_point_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for CUP_BOX_SCORE table
ALTER TABLE CUP_BOX_SCORE
    ADD CONSTRAINT fk_cup_box_score_players FOREIGN KEY (season_player_id) REFERENCES CUP_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_BOX_SCORE
    ADD CONSTRAINT fk_cup_box_score_header FOREIGN KEY (game_id) REFERENCES CUP_HEADER(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE CUP_BOX_SCORE
    ADD CONSTRAINT fk_cup_box_score_teams FOREIGN KEY (season_team_id) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_BOX_SCORE table
ALTER TABLE LIG_BOX_SCORE
    ADD CONSTRAINT fk_lig_box_score_players FOREIGN KEY (season_player_id) REFERENCES LIG_PLAYERS(season_player_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_BOX_SCORE
    ADD CONSTRAINT fk_lig_box_score_header FOREIGN KEY (game_id) REFERENCES LIG_HEADER(game_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE LIG_BOX_SCORE
    ADD CONSTRAINT fk_lig_box_score_teams FOREIGN KEY (season_team_id) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for CUP_PLAYERS table
ALTER TABLE CUP_PLAYERS
    ADD CONSTRAINT fk_cup_players_teams FOREIGN KEY (season_team_id) REFERENCES CUP_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Adding Foreign Keys for LIG_PLAYERS table
ALTER TABLE LIG_PLAYERS
    ADD CONSTRAINT fk_lig_players_teams FOREIGN KEY (season_team_id) REFERENCES LIG_TEAMS(season_team_id) ON DELETE CASCADE ON UPDATE CASCADE;