from dataclasses import dataclass
from db.db import db
import mysql.connector

@dataclass
class CupPlayByPlay:
    game_play_id: str
    game_id: str
    game: str
    round: str
    phase: str
    season_code: str
    quarter: str
    type: str
    number_of_play: int
    team_id: str
    player_id: str
    play_type: str
    player: str
    team: str
    dorsal: int
    minute: str
    marker_time: str
    points_a: int
    points_b: int
    comment: str
    play_info: str


class CupPlayByPlayDAO:
    @staticmethod
    def create_play(db: db, play: CupPlayByPlay) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            query = """
                INSERT INTO cup_play_by_play (
                    game_play_id, game_id, game, round, phase, season_code,
                    quarter, type, number_of_play, team_id, player_id, play_type,
                    player, team, dorsal, minute, marker_time, points_a, points_b,
                    comment, play_info
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                play.game_play_id, play.game_id, play.game, play.round, play.phase,
                play.season_code, play.quarter, play.type, play.number_of_play,
                play.team_id, play.player_id, play.play_type, play.player,
                play.team, play.dorsal, play.minute, play.marker_time,
                play.points_a, play.points_b, play.comment, play.play_info
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_play(db: db, game_play_id: str) -> CupPlayByPlay:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            query = "SELECT * FROM cup_play_by_play WHERE game_play_id = %s"
            cursor.execute(query, (game_play_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return CupPlayByPlay(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_plays(db: db) -> list:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            query = "SELECT * FROM cup_play_by_play"
            cursor.execute(query)
            plays = cursor.fetchall()
            return [CupPlayByPlay(*play) for play in plays]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_play(db: db, play: CupPlayByPlay) -> None:
        try:
            connection = db.get_connection()
            query = """
                UPDATE cup_play_by_play SET
                    game_id = %s, game = %s, round = %s, phase = %s,
                    season_code = %s, quarter = %s, type = %s,
                    number_of_play = %s, team_id = %s, player_id = %s,
                    play_type = %s, player = %s, team = %s, dorsal = %s,
                    minute = %s, marker_time = %s, points_a = %s, points_b = %s,
                    comment = %s, play_info = %s
                WHERE game_play_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (
                play.game_id, play.game, play.round, play.phase, play.season_code,
                play.quarter, play.type, play.number_of_play, play.team_id,
                play.player_id, play.play_type, play.player, play.team, play.dorsal,
                play.minute, play.marker_time, play.points_a, play.points_b,
                play.comment, play.play_info, play.game_play_id
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_play(db: db, game_play_id: str) -> None:
        try:
            connection = db.get_connection()
            query = "DELETE FROM cup_play_by_play WHERE game_play_id = %s"
            cursor = connection.cursor()
            cursor.execute(query, (game_play_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

