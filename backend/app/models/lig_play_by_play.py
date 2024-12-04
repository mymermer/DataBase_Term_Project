from dataclasses import dataclass
from datetime import datetime
from db.db import db
import mysql.connector

@dataclass
class LigPlayByPlay:
    game_play_id: str
    game_player_id: str
    game_point_id: str
    game_id: str
    game: str
    round_of_game: int
    phase: str
    season_player_id: str
    season_team_id: str
    quarter: str
    play_type: str
    player: str
    team: str
    dorsal: int
    minute: int
    points_a: int
    points_b: int
    play_info: str

class LigPlayByPlayDAO:
    @staticmethod
    def create_play(db: db, play: LigPlayByPlay) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            query = """
                INSERT INTO LIG_PLAY_BY_PLAY (
                    game_play_id, game_player_id, game_point_id, game_id, game, round_of_game, phase,
                    season_player_id, season_team_id, quarter, play_type, player, team, dorsal,
                    minute, points_a, points_b, play_info
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                play.game_play_id, play.game_player_id, play.game_point_id, play.game_id, play.game,
                play.round_of_game, play.phase, play.season_player_id, play.season_team_id, play.quarter,
                play.play_type, play.player, play.team, play.dorsal, play.minute,
                play.points_a, play.points_b, play.play_info
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_play(db: db, game_play_id: str) -> LigPlayByPlay:
        try:
            connection = db.get_connection()
            query = """
            SELECT * FROM LIG_PLAY_BY_PLAY WHERE game_play_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_play_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return LigPlayByPlay(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_plays(db: db) -> list[LigPlayByPlay]:
        try:
            connection = db.get_connection()
            query = """
            SELECT * FROM LIG_PLAY_BY_PLAY
            """
            cursor = connection.cursor()
            cursor.execute(query)
            plays = cursor.fetchall()
            return [LigPlayByPlay(*play) for play in plays]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_play(db: db, play: LigPlayByPlay) -> None:
        try:
            connection = db.get_connection()
            query = """
                UPDATE LIG_PLAY_BY_PLAY SET
                    game_player_id = %s, game_point_id = %s, game_id = %s, game = %s,
                    round_of_game = %s, phase = %s, season_player_id = %s, season_team_id = %s,
                    quarter = %s, play_type = %s, player = %s, team = %s, dorsal = %s,
                    minute = %s, points_a = %s, points_b = %s, play_info = %s
                WHERE game_play_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (
                play.game_player_id, play.game_point_id, play.game_id, play.game,
                play.round_of_game, play.phase, play.season_player_id, play.season_team_id,
                play.quarter, play.play_type, play.player, play.team, play.dorsal,
                play.minute, play.points_a, play.points_b, play.play_info, play.game_play_id
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
            query = """
            DELETE FROM LIG_PLAY_BY_PLAY WHERE game_play_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_play_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
