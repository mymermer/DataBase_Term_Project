from dataclasses import dataclass
from datetime import datetime
from db.db import db
import mysql.connector

# game_point_id VARCHAR(50) PRIMARY KEY,
# game_player_id VARCHAR(50),
# game_play_id VARCHAR(50),
# game_id VARCHAR(50),
# game VARCHAR(50),
# round_of_game INT,
# phase VARCHAR(50),
# season_player_id VARCHAR(50),
# season_team_id VARCHAR(50),
# player VARCHAR(50),
# action_id VARCHAR(50),
# action_of_play VARCHAR(50),
# points INT,
# coord_x INT,
# coord_y INT,
# zone_of_play CHAR(1),
# minute INT,
# points_a INT,
# points_b INT,
# date_time_stp DATETIME

@dataclass
class Cup_Points:
    game_point_id: str
    game_player_id: str
    game_play_id: str
    game_id: str
    game: str
    round_of_game: int
    phase: str
    season_player_id: str
    season_team_id: str
    player: str
    action_id: str
    action_of_play: str
    points: int
    coord_x: int
    coord_y: int
    zone_of_play: str
    minute: int
    points_a: int
    points_b: int
    date_time_stp: datetime

class Cup_PointsDAO():
    @staticmethod
    def create_cup_points(db: db, point: Cup_Points) -> None:
        try:
            connection  = db.get_connection()
            cursor = db.connection.cursor()
            query = """
                INSERT INTO CUP_POINTS (
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
                ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """

            cursor.execute(query, (
                point.game_point_id,
                point.game_player_id,
                point.game_play_id,
                point.game_id,
                point.game,
                point.round_of_game,
                point.phase,
                point.season_player_id,
                point.season_team_id,
                point.player,
                point.action_id,
                point.action_of_play,
                point.points,
                point.coord_x,
                point.coord_y,
                point.zone_of_play,
                point.minute,
                point.points_a,
                point.points_b,
                point.date_time_stp
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_cup_points(db: db, game_point_id: str) -> Cup_Points:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM CUP_POINTS WHERE game_point_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_point_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return Cup_Points(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_all_cup_points(db: db) -> list:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM CUP_POINTS
            """
            cursor = connection.cursor()
            cursor.execute(query)
            points = cursor.fetchall()
            if points is None:
                return None
            #! special return might not be needed but we will see
            return [Cup_Points(*point) for point in points]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()  
    
    
    @staticmethod
    def update_cup_points(db: db, point: Cup_Points) -> None:
        try:
            connection = db.get_connection()
            query = """
            UPDATE CUP_POINTS SET
            game_player_id = %s,
            game_play_id = %s,
            game_id = %s,
            game = %s,
            round_of_game = %s,
            phase = %s,
            season_player_id = %s,
            season_team_id = %s,
            player = %s,
            action_id = %s,
            action_of_play = %s,
            points = %s,
            coord_x = %s,
            coord_y = %s,
            zone_of_play = %s,
            minute = %s,
            points_a = %s,
            points_b = %s,
            date_time_stp = %s
            WHERE game_point_id = %s
            """

            cursor = connection.cursor()
            cursor.execute(query, (
                point.game_player_id,
                point.game_play_id,
                point.game_id,
                point.game,
                point.round_of_game,
                point.phase,
                point.season_player_id,
                point.season_team_id,
                point.player,
                point.action_id,
                point.action_of_play,
                point.points,
                point.coord_x,
                point.coord_y,
                point.zone_of_play,
                point.minute,
                point.points_a,
                point.points_b,
                point.date_time_stp,
                point.game_point_id  # Identifier for WHERE clause
            ))

            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_cup_points(db: db, game_point_id: str) -> None:
        try:
            connection = db.get_connection()
            query = """
                DELETE FROM CUP_POINTS WHERE game_point_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_point_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()