-- Cleaning up CUP_POINTS table
DELETE FROM CUP_POINTS
WHERE season_team_id NOT IN (SELECT season_team_id FROM CUP_TEAMS)
   OR game_id NOT IN (SELECT game_id FROM CUP_HEADER)
   OR game_play_id NOT IN (SELECT game_play_id FROM CUP_PLAY_BY_PLAY)
   OR game_player_id NOT IN (SELECT game_player_id FROM CUP_BOX_SCORE)
   OR season_player_id NOT IN (SELECT season_player_id FROM CUP_PLAYERS);

-- Cleaning up LIG_POINTS table
DELETE FROM LIG_POINTS
WHERE season_team_id NOT IN (SELECT season_team_id FROM LIG_TEAMS)
   OR game_id NOT IN (SELECT game_id FROM LIG_HEADER)
   OR game_play_id NOT IN (SELECT game_play_id FROM LIG_PLAY_BY_PLAY)
   OR game_player_id NOT IN (SELECT game_player_id FROM LIG_BOX_SCORE)
   OR season_player_id NOT IN (SELECT season_player_id FROM LIG_PLAYERS);

-- Cleaning up CUP_COMPARISON table
DELETE FROM CUP_COMPARISON
WHERE game_id NOT IN (SELECT game_id FROM CUP_HEADER)
   OR season_team_id_a NOT IN (SELECT season_team_id FROM CUP_TEAMS)
   OR season_team_id_b NOT IN (SELECT season_team_id FROM CUP_TEAMS);

-- Cleaning up LIG_COMPARISON table
DELETE FROM LIG_COMPARISON
WHERE game_id NOT IN (SELECT game_id FROM LIG_HEADER)
   OR season_team_id_a NOT IN (SELECT season_team_id FROM LIG_TEAMS)
   OR season_team_id_b NOT IN (SELECT season_team_id FROM LIG_TEAMS);

-- Cleaning up CUP_HEADER table
DELETE FROM CUP_HEADER
WHERE season_team_id_a NOT IN (SELECT season_team_id FROM CUP_TEAMS)
   OR season_team_id_b NOT IN (SELECT season_team_id FROM CUP_TEAMS);

-- Cleaning up LIG_HEADER table
DELETE FROM LIG_HEADER
WHERE season_team_id_a NOT IN (SELECT season_team_id FROM LIG_TEAMS)
   OR season_team_id_b NOT IN (SELECT season_team_id FROM LIG_TEAMS);

-- Cleaning up CUP_PLAY_BY_PLAY table
DELETE FROM CUP_PLAY_BY_PLAY
WHERE game_id NOT IN (SELECT game_id FROM CUP_HEADER)
   OR season_team_id NOT IN (SELECT season_team_id FROM CUP_TEAMS)
   OR game_player_id NOT IN (SELECT game_player_id FROM CUP_BOX_SCORE)
   OR season_player_id NOT IN (SELECT season_player_id FROM CUP_PLAYERS)
   OR game_point_id NOT IN (SELECT game_point_id FROM CUP_POINTS);

-- Cleaning up LIG_PLAY_BY_PLAY table
DELETE FROM LIG_PLAY_BY_PLAY
WHERE game_id NOT IN (SELECT game_id FROM LIG_HEADER)
   OR season_team_id NOT IN (SELECT season_team_id FROM LIG_TEAMS)
   OR game_player_id NOT IN (SELECT game_player_id FROM LIG_BOX_SCORE)
   OR season_player_id NOT IN (SELECT season_player_id FROM LIG_PLAYERS)
   OR game_point_id NOT IN (SELECT game_point_id FROM LIG_POINTS);

-- Cleaning up CUP_BOX_SCORE table
DELETE FROM CUP_BOX_SCORE
WHERE season_player_id NOT IN (SELECT season_player_id FROM CUP_PLAYERS)
   OR game_id NOT IN (SELECT game_id FROM CUP_HEADER)
   OR season_team_id NOT IN (SELECT season_team_id FROM CUP_TEAMS);

-- Cleaning up LIG_BOX_SCORE table
DELETE FROM LIG_BOX_SCORE
WHERE season_player_id NOT IN (SELECT season_player_id FROM LIG_PLAYERS)
   OR game_id NOT IN (SELECT game_id FROM LIG_HEADER)
   OR season_team_id NOT IN (SELECT season_team_id FROM LIG_TEAMS);

-- Cleaning up CUP_PLAYERS table
DELETE FROM CUP_PLAYERS
WHERE season_team_id NOT IN (SELECT season_team_id FROM CUP_TEAMS);

-- Cleaning up LIG_PLAYERS table
DELETE FROM LIG_PLAYERS
WHERE season_team_id NOT IN (SELECT season_team_id FROM LIG_TEAMS);
