from dataclasses import dataclass
from datetime import datetime
from app.db.db import db
import mysql.connector
from typing import Optional

@dataclass
class CupBoxScore:
    game_player_id: Optional[str] = None
    game_id: Optional[str] = None
    game: Optional[str] = None
    round_of_game: Optional[int] = None
    phase: Optional[str] = None
    season_player_id: Optional[str] = None
    season_team_id: Optional[str] = None
    is_starter: Optional[bool] = None
    is_playing: Optional[bool] = None
    dorsal: Optional[int] = None
    player: Optional[str] = None
    points: Optional[int] = None
    two_points_made: Optional[int] = None
    two_points_attempted: Optional[int] = None
    three_points_made: Optional[int] = None
    three_points_attempted: Optional[int] = None
    free_throws_made: Optional[int] = None
    free_throws_attempted: Optional[int] = None
    offensive_rebounds: Optional[int] = None
    defensive_rebounds: Optional[int] = None
    total_rebounds: Optional[int] = None
    assists: Optional[int] = None
    steals: Optional[int] = None
    turnovers: Optional[int] = None
    blocks_favour: Optional[int] = None
    blocks_against: Optional[int] = None
    fouls_committed: Optional[int] = None
    fouls_received: Optional[int] = None
    valuation: Optional[int] = None

class CupBoxScoreDAO:
    @staticmethod
    def create_cup_box_score(db: db, boxscore: CupBoxScore) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            if isinstance(boxscore, CupBoxScore):
                boxscore = boxscore.__dict__

            columns = ", ".join(boxscore.keys())
            placeholders = ", ".join(["%s"] * len(boxscore))
            query = f"INSERT INTO CUP_BOX_SCORE ({columns}) VALUES ({placeholders})"

            cursor.execute(query, list(boxscore.values()))
            connection.commit()
            print("Successfully created CUP_BOX_SCORE with provided data.")
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            if connection:
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
    def get_cup_box_score(db: db, game_player_id: str) -> CupBoxScore:
        try:
            connection = db.get_connection()
            query = """
            SELECT * FROM CUP_BOX_SCORE WHERE game_player_id = %s 
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_player_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return CupBoxScore(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_cup_box_scores(db: db) -> list:
        try:
            connection = db.get_connection()
            query = """
            SELECT * FROM CUP_BOX_SCORE
            """
            cursor = connection.cursor()
            cursor.execute(query)
            box_scores = cursor.fetchall() 
            if box_scores is None:
                return None
            return [CupBoxScore(*boxscore) for boxscore in box_scores]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_cup_box_score(db: db, boxscore: CupBoxScore) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            fields_to_update = {}
            if boxscore.game_player_id is not None:
                fields_to_update['game_player_id'] = boxscore.game_player_id
            if boxscore.game_id is not None:
                fields_to_update['game_id'] = boxscore.game_id
            if boxscore.game is not None:
                fields_to_update['game'] = boxscore.game
            if boxscore.round_of_game is not None:
                fields_to_update['round_of_game'] = boxscore.round_of_game
            if boxscore.phase is not None:
                fields_to_update['phase'] = boxscore.phase
            if boxscore.season_player_id is not None:
                fields_to_update['season_player_id'] = boxscore.season_player_id
            if boxscore.season_team_id is not None:
                fields_to_update['season_team_id'] = boxscore.season_team_id
            if boxscore.is_starter is not None:
                fields_to_update['is_starter'] = boxscore.is_starter
            if boxscore.is_playing is not None:
                fields_to_update['is_playing'] = boxscore.is_playing
            if boxscore.dorsal is not None:
                fields_to_update['dorsal'] = boxscore.dorsal
            if boxscore.player is not None:
                fields_to_update['player'] = boxscore.player
            if boxscore.points is not None:
                fields_to_update['points'] = boxscore.points
            if boxscore.two_points_made is not None:
                fields_to_update['two_points_made'] = boxscore.two_points_made
            if boxscore.two_points_attempted is not None:
                fields_to_update['two_points_attempted'] = boxscore.two_points_attempted
            if boxscore.three_points_made is not None:
                fields_to_update['three_points_made'] = boxscore.three_points_made
            if boxscore.three_points_attempted is not None:
                fields_to_update['three_points_attempted'] = boxscore.three_points_attempted
            if boxscore.free_throws_made is not None:
                fields_to_update['free_throws_made'] = boxscore.free_throws_made
            if boxscore.free_throws_attempted is not None:
                fields_to_update['free_throws_attempted'] = boxscore.free_throws_attempted
            if boxscore.offensive_rebounds is not None:
                fields_to_update['offensive_rebounds'] = boxscore.offensive_rebounds
            if boxscore.defensive_rebounds is not None:
                fields_to_update['defensive_rebounds'] = boxscore.defensive_rebounds
            if boxscore.total_rebounds is not None:
                fields_to_update['total_rebounds'] = boxscore.total_rebounds
            if boxscore.assists is not None:
                fields_to_update['assists'] = boxscore.assists
            if boxscore.steals is not None:
                fields_to_update['steals'] = boxscore.steals
            if boxscore.turnovers is not None:
                fields_to_update['turnovers'] = boxscore.turnovers
            if boxscore.blocks_favour is not None:
                fields_to_update['blocks_favour'] = boxscore.blocks_favour
            if boxscore.blocks_against is not None:
                fields_to_update['blocks_against'] = boxscore.blocks_against
            if boxscore.fouls_committed is not None:
                fields_to_update['fouls_committed'] = boxscore.fouls_committed
            if boxscore.fouls_received is not None:
                fields_to_update['fouls_received'] = boxscore.fouls_received
            if boxscore.valuation is not None:
                fields_to_update['valuation'] = boxscore.valuation

            if not fields_to_update:
                raise ValueError("No fields to update were provided.")

            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"""
                UPDATE CUP_BOX_SCORE
                SET {set_clause}
                WHERE game_player_id = %s
            """

            values = list(fields_to_update.values())
            values.append(boxscore.game_player_id)  

            cursor.execute(query, tuple(values))
            connection.commit()
        except Exception as err:
            print(f"Error: {err}")
            if connection:
                connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_cup_box_score(db: db, game_player_id: str) -> None:  
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            query = """
                DELETE FROM CUP_BOX_SCORE WHERE game_player_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_player_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            if connection:
                connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_paginated_cup_box_scores(
        db: db, offset: int = 0, limit: int = 25, columns: list = None, filters: dict = None, sort_by: str = None, order: str = 'asc') -> list: 
        try:
            connection = db.get_connection()
            selected_columns = ", ".join(columns) if columns else "*"
            where_clauses = []
            params = []

            if filters:
                for column, value in filters.items():
                    where_clauses.append(f"{column} = %s")
                    params.append(value)

            where_clause = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

            order_clause = ""
            if sort_by:
                if order.lower() not in ['asc', 'desc']:
                    order = 'asc'
                order_clause = f"ORDER BY {sort_by} {order.upper()}"
            query = f"""
                SELECT {selected_columns} 
                FROM CUP_BOX_SCORE
                {where_clause}
                {order_clause}
                LIMIT %s OFFSET %s
            """        
            
            params.extend([limit, offset])
            cursor = connection.cursor()
            cursor.execute(query, params)
            box_scores = cursor.fetchall()

            if box_scores is None:
                return None

            if columns:
                return [dict(zip(columns, box_score)) for box_score in box_scores]
            else:
                return [CupBoxScore(*box_score) for box_score in box_scores] 
        except mysql.connector.Error as err:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_total_cup_box_scores(db: db, filters: dict = None) -> int:  
        try:
            connection = db.get_connection()
            where_clauses = []
            params = []

            if filters:
                for column, value in filters.items():
                    where_clauses.append(f"{column} = %s")
                    params.append(value)

            where_clause = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
            
            query = f"""
                SELECT COUNT(*) FROM CUP_BOX_SCORE
                {where_clause}
            """

            cursor = connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()

            if result:
                return result[0]
            else:
                raise ValueError("Query returned no results.")
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            raise
        except Exception as e:
            print(f"Unexpected Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()