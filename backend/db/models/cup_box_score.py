from dataclasses import dataclass
from db.db import db
import mysql.connector

@dataclass
class CupBoxscore:
    cup_box_score_id: str
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


class CupBoxscoresDAO:
    @staticmethod
    def create_cup_box_score(db: db, cup_box_score: CupBoxscore) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            query = """
                INSERT INTO cup_box_score (
                    cup_box_score_id, game_id, game, round, phase, season_code,
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
                cup_box_score.cup_box_score_id, cup_box_score.game_id, cup_box_score.game,
                cup_box_score.round, cup_box_score.phase, cup_box_score.season_code,
                cup_box_score.player_id, cup_box_score.is_starter, cup_box_score.is_playing,
                cup_box_score.team_id, cup_box_score.dorsal, cup_box_score.player,
                cup_box_score.minutes, cup_box_score.points, cup_box_score.two_points_made,
                cup_box_score.two_points_attempted, cup_box_score.three_points_made,
                cup_box_score.three_points_attempted, cup_box_score.free_throws_made,
                cup_box_score.free_throws_attempted, cup_box_score.offensive_rebounds,
                cup_box_score.defensive_rebounds, cup_box_score.total_rebounds,
                cup_box_score.assists, cup_box_score.steals, cup_box_score.turnovers,
                cup_box_score.blocks_favour, cup_box_score.blocks_against,
                cup_box_score.fouls_committed, cup_box_score.fouls_received,
                cup_box_score.valuation, cup_box_score.plus_minus
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_cup_box_score(db: db, cup_box_score_id: str) -> CupBoxscore:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM cup_box_score WHERE cup_box_score_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (cup_box_score_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return CupBoxscore(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_cup_box_scores(db: db) -> list:
        try:
            connection = db.get_connection()
            query = "SELECT * FROM cup_box_score"
            cursor = connection.cursor()
            cursor.execute(query)
            box_scores = cursor.fetchall()
            return [CupBoxscore(*box_score) for box_score in box_scores]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_cup_box_score(db: db, cup_box_score: CupBoxscore) -> None:
        try:
            connection = db.get_connection()
            query = """
                UPDATE cup_box_score SET
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
                WHERE cup_box_score_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (
                cup_box_score.game_id, cup_box_score.game, cup_box_score.round,
                cup_box_score.phase, cup_box_score.season_code, cup_box_score.player_id,
                cup_box_score.is_starter, cup_box_score.is_playing, cup_box_score.team_id,
                cup_box_score.dorsal, cup_box_score.player, cup_box_score.minutes,
                cup_box_score.points, cup_box_score.two_points_made,
                cup_box_score.two_points_attempted, cup_box_score.three_points_made,
                cup_box_score.three_points_attempted, cup_box_score.free_throws_made,
                cup_box_score.free_throws_attempted, cup_box_score.offensive_rebounds,
                cup_box_score.defensive_rebounds, cup_box_score.total_rebounds,
                cup_box_score.assists, cup_box_score.steals, cup_box_score.turnovers,
                cup_box_score.blocks_favour, cup_box_score.blocks_against,
                cup_box_score.fouls_committed, cup_box_score.fouls_received,
                cup_box_score.valuation, cup_box_score.plus_minus,
                cup_box_score.cup_box_score_id
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_cup_box_score(db: db, cup_box_score_id: str) -> None:
        try:
            connection = db.get_connection()
            query = "DELETE FROM cup_box_score WHERE cup_box_score_id = %s"
            cursor = connection.cursor()
            cursor.execute(query, (cup_box_score_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
