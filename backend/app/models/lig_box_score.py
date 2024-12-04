from dataclasses import dataclass
from datetime import datetime
from db.db import db
import mysql.connector

@dataclass
class LigBoxScore:
    game_player_id: str
    game_id: str
    game: str
    round_of_game: int
    phase: str
    season_player_id: str
    season_team_id: str
    is_starter: bool
    is_playing: bool
    dorsal: int
    player: str
    points: int
    two_points_made: int
    two_points_attempted: int
    three_points_made: int
    three_points_attempted: int
    free_throws_made: int
    free_throws_attempted: int
    offensive_rebounds: int
    defensive_rebounds: int
    total_rebounds: int
    assists: int
    steals: int
    turnovers: int
    blocks_favour: int
    blocks_against: int
    fouls_committed: int
    fouls_received: int
    valuation: int

class LigBoxScoreDAO:
    @staticmethod
    def create_lig_box_score(db: db, boxscore: LigBoxScore) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            query = """
                INSERT INTO LIG_BOX_SCORE (
                    game_player_id, game_id, game, round_of_game, phase, season_player_id, season_team_id,
                    is_starter, is_playing, dorsal, player, points, two_points_made, two_points_attempted,
                    three_points_made, three_points_attempted, free_throws_made, free_throws_attempted,
                    offensive_rebounds, defensive_rebounds, total_rebounds, assists, steals, turnovers,
                    blocks_favour, blocks_against, fouls_committed, fouls_received, valuation
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            cursor.execute(query, (
                boxscore.game_player_id, boxscore.game_id, boxscore.game, boxscore.round_of_game,
                boxscore.phase, boxscore.season_player_id, boxscore.season_team_id,
                boxscore.is_starter, boxscore.is_playing, boxscore.dorsal, boxscore.player,
                boxscore.points, boxscore.two_points_made, boxscore.two_points_attempted,
                boxscore.three_points_made, boxscore.three_points_attempted,
                boxscore.free_throws_made, boxscore.free_throws_attempted,
                boxscore.offensive_rebounds, boxscore.defensive_rebounds, boxscore.total_rebounds,
                boxscore.assists, boxscore.steals, boxscore.turnovers,
                boxscore.blocks_favour, boxscore.blocks_against,
                boxscore.fouls_committed, boxscore.fouls_received, boxscore.valuation
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_lig_box_score(db: db, game_player_id: str) -> LigBoxScore:
        try:
            connection = db.get_connection()
            query = """
            SELECT * FROM LIG_BOX_SCORE WHERE game_player_id = %s 
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_player_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return LigBoxScore(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_lig_box_score(db: db) -> list[LigBoxScore]:
        try:
            connection = db.get_connection()
            query = """
            SELECT * FROM LIG_BOX_SCORE
            """
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return [LigBoxScore(*row) for row in results]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_lig_box_score(db: db, boxscore: LigBoxScore) -> None:
        try:
            connection = db.get_connection()
            query = """
                UPDATE LIG_BOX_SCORE SET
                    game_id = %s, game = %s, round_of_game = %s, phase = %s, season_player_id = %s,
                    season_team_id = %s, is_starter = %s, is_playing = %s, dorsal = %s, player = %s,
                    points = %s, two_points_made = %s, two_points_attempted = %s,
                    three_points_made = %s, three_points_attempted = %s,
                    free_throws_made = %s, free_throws_attempted = %s,
                    offensive_rebounds = %s, defensive_rebounds = %s, total_rebounds = %s,
                    assists = %s, steals = %s, turnovers = %s, blocks_favour = %s,
                    blocks_against = %s, fouls_committed = %s, fouls_received = %s, valuation = %s
                WHERE game_player_id = %s
            """
            cursor.execute(query, (
                boxscore.game_id, boxscore.game, boxscore.round_of_game, boxscore.phase,
                boxscore.season_player_id, boxscore.season_team_id, boxscore.is_starter,
                boxscore.is_playing, boxscore.dorsal, boxscore.player, boxscore.points,
                boxscore.two_points_made, boxscore.two_points_attempted, boxscore.three_points_made,
                boxscore.three_points_attempted, boxscore.free_throws_made, boxscore.free_throws_attempted,
                boxscore.offensive_rebounds, boxscore.defensive_rebounds, boxscore.total_rebounds,
                boxscore.assists, boxscore.steals, boxscore.turnovers, boxscore.blocks_favour,
                boxscore.blocks_against, boxscore.fouls_committed, boxscore.fouls_received,
                boxscore.valuation, boxscore.game_player_id
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_lig_box_score(db: db, game_player_id: str) -> None:
        try:
            connection = db.get_connection()
            query = """
            DELETE FROM LIG_BOX_SCORE WHERE game_player_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_player_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
