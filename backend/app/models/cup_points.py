from dataclasses import dataclass
from datetime import datetime
from app.db.db import db
import mysql.connector
from typing import Optional, Any, Dict

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
            cursor = connection.cursor()
            
            # Extract fields from the `point` object
            fields_to_update = {}
            if point.game_player_id is not None:
                fields_to_update['game_player_id'] = point.game_player_id
            if point.game_play_id is not None:
                fields_to_update['game_play_id'] = point.game_play_id
            if point.game_id is not None:
                fields_to_update['game_id'] = point.game_id
            if point.game is not None:
                fields_to_update['game'] = point.game
            if point.round_of_game is not None:
                fields_to_update['round_of_game'] = point.round_of_game
            if point.phase is not None:
                fields_to_update['phase'] = point.phase
            if point.season_player_id is not None:
                fields_to_update['season_player_id'] = point.season_player_id
            if point.season_team_id is not None:
                fields_to_update['season_team_id'] = point.season_team_id
            if point.player is not None:
                fields_to_update['player'] = point.player
            if point.action_id is not None:
                fields_to_update['action_id'] = point.action_id
            if point.action_of_play is not None:
                fields_to_update['action_of_play'] = point.action_of_play
            if point.points is not None:
                fields_to_update['points'] = point.points
            if point.coord_x is not None:
                fields_to_update['coord_x'] = point.coord_x
            if point.coord_y is not None:
                fields_to_update['coord_y'] = point.coord_y
            if point.zone_of_play is not None:
                fields_to_update['zone_of_play'] = point.zone_of_play
            if point.minute is not None:
                fields_to_update['minute'] = point.minute
            if point.points_a is not None:
                fields_to_update['points_a'] = point.points_a
            if point.points_b is not None:
                fields_to_update['points_b'] = point.points_b
            if point.date_time_stp is not None:
                fields_to_update['date_time_stp'] = point.date_time_stp
            
            # Construct dynamic SQL query
            if not fields_to_update:
                raise ValueError("No fields to update were provided.")
            
            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"""
            UPDATE CUP_POINTS
            SET {set_clause}
            WHERE game_point_id = %s
            """
            
            # Prepare values for the query
            values = list(fields_to_update.values())
            values.append(point.game_point_id)  # Add identifier for WHERE clause

            # Execute query
            cursor.execute(query, tuple(values))
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