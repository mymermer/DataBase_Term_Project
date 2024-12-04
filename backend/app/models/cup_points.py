from dataclasses import dataclass
from datetime import datetime
from app.db.db import db
import mysql.connector
from typing import Optional

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
    game_point_id: Optional[str] = None
    game_player_id: Optional[str] = None
    game_play_id: Optional[str] = None
    game_id: Optional[str] = None
    game: Optional[str] = None
    round_of_game: Optional[int] = None
    phase: Optional[str] = None
    season_player_id: Optional[str] = None
    season_team_id: Optional[str] = None
    player: Optional[str] = None
    action_id: Optional[str] = None
    action_of_play: Optional[str] = None
    points: Optional[int] = None
    coord_x: Optional[int] = None
    coord_y: Optional[int] = None
    zone_of_play: Optional[str] = None
    minute: Optional[int] = None
    points_a: Optional[int] = None
    points_b: Optional[int] = None
    date_time_stp: Optional[datetime] = None

class Cup_PointsDAO:
    @staticmethod
    def create_cup_points(db, point):
        """
        Insert a new CUP_POINTS record with only provided columns.

        Args:
            db: Database connection.
            point: A `Cup_Points` object or dictionary containing column-value pairs for the record.
        """
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            # Convert Cup_Points object to dictionary if necessary
            if isinstance(point, Cup_Points):
                point = point.__dict__

            # Dynamically construct query based on provided keys
            columns = ", ".join(point.keys())
            placeholders = ", ".join(["%s"] * len(point))
            query = f"INSERT INTO CUP_POINTS ({columns}) VALUES ({placeholders})"

            # Execute query with provided values
            cursor.execute(query, list(point.values()))
            connection.commit()

            print(f"Successfully created CUP_POINTS with provided data.")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            connection.rollback()
            raise
        except Exception as e:
            print(f"General Error: {e}")
            raise
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
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