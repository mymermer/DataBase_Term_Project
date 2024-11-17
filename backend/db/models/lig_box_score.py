from dataclasses import dataclass
from db.db import db
import mysql.connector


@dataclass
class LigBoxscore:
    lig_box_score_id: str
    game_id: str
    game: str
    round: str
    phase: str
    season_code: str
    player_id: str
    is_starter: bool
    is_playing: bool
    team_id: str
    dorsal: int
    player: str
    minutes: float
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
    plus_minus: float


class LigBoxscoresDAO:
    @staticmethod
    def create_lig_box_score(db: db, lig_box_score: LigBoxscore) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            query = """
                INSERT INTO lig_box_score (
                    lig_box_score_id, game_id, game, round, phase, season_code,
                    player_id, is_starter, is_playing, team_id, dorsal, player,
                    minutes, points, two_points_made, two_points_attempted,
                    three_points_made, three_points_attempted, free_throws_made,
                    free_throws_attempted, offensive_rebounds, defensive_rebounds,
                    total_rebounds, assists, steals, turnovers, blocks_favour,
                    blocks_against, fouls_committed, fouls_received, valuation,
                    plus_minus
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                lig_box_score.lig_box_score_id, lig_box_score.game_id, lig_box_score.game,
                lig_box_score.round, lig_box_score.phase, lig_box_score.season_code,
                lig_box_score.player_id, lig_box_score.is_starter, lig_box_score.is_playing,
                lig_box_score.team_id, lig_box_score.dorsal, lig_box_score.player,
                lig_box_score.minutes, lig_box_score.points, lig_box_score.two_points_made,
                lig_box_score.two_points_attempted, lig_box_score.three_points_made,
                lig_box_score.three_points_attempted, lig_box_score.free_throws_made,
                lig_box_score.free_throws_attempted, lig_box_score.offensive_rebounds,
                lig_box_score.defensive_rebounds, lig_box_score.total_rebounds,
                lig_box_score.assists, lig_box_score.steals, lig_box_score.turnovers,
                lig_box_score.blocks_favour, lig_box_score.blocks_against,
                lig_box_score.fouls_committed, lig_box_score.fouls_received,
                lig_box_score.valuation, lig_box_score.plus_minus
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_lig_box_score(db: db, lig_box_score_id: str) -> LigBoxscore:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM lig_box_score WHERE lig_box_score_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (lig_box_score_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return LigBoxscore(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_lig_box_scores(db: db) -> list:
        try:
            connection = db.get_connection()
            query = "SELECT * FROM lig_box_score"
            cursor = connection.cursor()
            cursor.execute(query)
            box_scores = cursor.fetchall()
            return [LigBoxscore(*box_score) for box_score in box_scores]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_lig_box_score(db: db, lig_box_score: LigBoxscore) -> None:
        try:
            connection = db.get_connection()
            query = """
                UPDATE lig_box_score SET
                    game_id = %s, game = %s, round = %s, phase = %s,
                    season_code = %s, player_id = %s, is_starter = %s,
                    is_playing = %s, team_id = %s, dorsal = %s, player = %s,
                    minutes = %s, points = %s, two_points_made = %s,
                    two_points_attempted = %s, three_points_made = %s,
                    three_points_attempted = %s, free_throws_made = %s,
                    free_throws_attempted = %s, offensive_rebounds = %s,
                    defensive_rebounds = %s, total_rebounds = %s, assists = %s,
                    steals = %s, turnovers = %s, blocks_favour = %s,
                    blocks_against = %s, fouls_committed = %s,
                    fouls_received = %s, valuation = %s, plus_minus = %s
                WHERE lig_box_score_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (
                lig_box_score.game_id, lig_box_score.game, lig_box_score.round,
                lig_box_score.phase, lig_box_score.season_code, lig_box_score.player_id,
                lig_box_score.is_starter, lig_box_score.is_playing, lig_box_score.team_id,
                lig_box_score.dorsal, lig_box_score.player, lig_box_score.minutes,
                lig_box_score.points, lig_box_score.two_points_made,
                lig_box_score.two_points_attempted, lig_box_score.three_points_made,
                lig_box_score.three_points_attempted, lig_box_score.free_throws_made,
                lig_box_score.free_throws_attempted, lig_box_score.offensive_rebounds,
                lig_box_score.defensive_rebounds, lig_box_score.total_rebounds,
                lig_box_score.assists, lig_box_score.steals, lig_box_score.turnovers,
                lig_box_score.blocks_favour, lig_box_score.blocks_against,
                lig_box_score.fouls_committed, lig_box_score.fouls_received,
                lig_box_score.valuation, lig_box_score.plus_minus,
                lig_box_score.lig_box_score_id
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_lig_box_score(db: db, lig_box_score_id: str) -> None:
        try:
            connection = db.get_connection()
            query = "DELETE FROM lig_box_score WHERE lig_box_score_id = %s"
            cursor = connection.cursor()
            cursor.execute(query, (lig_box_score_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()