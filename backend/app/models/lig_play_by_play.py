from dataclasses import dataclass
from datetime import datetime
from app.db.db import db
import mysql.connector
from typing import Optional

@dataclass
class LigPlayByPlay:
    game_play_id: Optional[str] = None
    game_player_id: Optional[str] = None
    game_point_id: Optional[str] = None
    game_id: Optional[str] = None
    game: Optional[str] = None
    round_of_game: Optional[int] = None
    phase: Optional[str] = None
    season_player_id: Optional[str] = None
    season_team_id: Optional[str] = None
    quarter: Optional[str] = None
    play_type: Optional[str] = None
    player: Optional[str] = None
    team: Optional[str] = None
    dorsal: Optional[int] = None
    minute: Optional[int] = None
    points_a: Optional[int] = None
    points_b: Optional[int] = None
    play_info: Optional[str] = None

class LigPlayByPlayDAO:
    @staticmethod
    def create_play(db: db, play: LigPlayByPlay) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            if isinstance(play, LigPlayByPlay):
                play = play.__dict__

            columns = ", ".join(play.keys())
            placeholders = ", ".join(["%s"] * len(play))
            query = f"INSERT INTO LIG_PLAY_BY_PLAY ({columns}) VALUES ({placeholders})"

            cursor.execute(query, list(play.values()))
            connection.commit()

            print(f"Successfully created LIG_PLAY_BY_PLAY with provided data.")

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
    def update_play(db: db, play: LigPlayByPlay) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            
            fields_to_update = {}
            for field, value in play.__dict__.items():
                if value is not None and field != 'game_play_id':
                    fields_to_update[field] = value
            
            if not fields_to_update:
                raise ValueError("No fields to update were provided.")
            
            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"""
            UPDATE LIG_PLAY_BY_PLAY
            SET {set_clause}
            WHERE game_play_id = %s
            """
            
            values = list(fields_to_update.values())
            values.append(play.game_play_id)

            cursor.execute(query, tuple(values))
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
    def get_all_plays(db: db) -> list:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM LIG_PLAY_BY_PLAY
            """
            cursor = connection.cursor()
            cursor.execute(query)
            plays = cursor.fetchall()
            if plays is None:
                return None
            return [LigPlayByPlay(*play) for play in plays]
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

    @staticmethod
    def get_paginated_plays(db: db, offset: int = 0, limit: int = 25, columns: list = None, filters: dict = None) -> list:
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
            
            query = f"""
                SELECT {selected_columns} FROM LIG_PLAY_BY_PLAY
                {where_clause}
                LIMIT %s OFFSET %s
            """
            
            params.extend([limit, offset])
            
            cursor = connection.cursor()
            cursor.execute(query, params)
            plays = cursor.fetchall()

            if plays is None:
                return None

            if columns:
                return [dict(zip(columns, play)) for play in plays]
            else:
                return [LigPlayByPlay(*play) for play in plays]
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_total_plays(db: db, filters: dict = None) -> int:
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
                SELECT COUNT(*) FROM LIG_PLAY_BY_PLAY
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