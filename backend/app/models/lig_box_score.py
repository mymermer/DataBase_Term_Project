from dataclasses import dataclass
from datetime import datetime
from app.db.db import db
import mysql.connector
from typing import Optional, List, Dict

@dataclass
class LigBoxScore:
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

class LigBoxScoreDAO:
    @staticmethod
    def create_lig_box_score(db: db, boxscore: LigBoxScore) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            if isinstance(boxscore, LigBoxScore):
                boxscore = boxscore.__dict__

            columns = ", ".join(boxscore.keys())
            placeholders = ", ".join(["%s"] * len(boxscore))
            query = f"INSERT INTO LIG_BOX_SCORE ({columns}) VALUES ({placeholders})"

            cursor.execute(query, list(boxscore.values()))
            connection.commit()
            print("Successfully created LigBoxScore with provided data.")
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
    def get_lig_box_score(db: db, game_player_id: str) -> Optional[LigBoxScore]:
        try:
            connection = db.get_connection()
            query = "SELECT * FROM LIG_BOX_SCORE WHERE game_player_id = %s"
            cursor = connection.cursor()
            cursor.execute(query, (game_player_id,))
            result = cursor.fetchone()
            return LigBoxScore(*result) if result else None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    @staticmethod
    def get_all_lig_box_scores(db: db) -> List[LigBoxScore]:
        try:
            connection = db.get_connection()
            query = "SELECT * FROM LIG_BOX_SCORE"
            cursor = connection.cursor()
            cursor.execute(query)
            box_scores = cursor.fetchall()
            return [LigBoxScore(*row) for row in box_scores]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    @staticmethod
    def update_lig_box_score(db: db, boxscore: LigBoxScore) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            fields_to_update = {k: v for k, v in boxscore.__dict__.items() if v is not None and k != 'game_player_id'}
            if not fields_to_update:
                raise ValueError("No fields to update were provided.")

            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"UPDATE LIG_BOX_SCORE SET {set_clause} WHERE game_player_id = %s"

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
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    @staticmethod
    def delete_lig_box_score(db: db, game_player_id: str) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            query = "DELETE FROM LIG_BOX_SCORE WHERE game_player_id = %s"
            cursor.execute(query, (game_player_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            if connection:
                connection.rollback()
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    @staticmethod
    def get_paginated_lig_box_scores(
        db: db, offset: int = 0, limit: int = 25, columns: List[str] = None, filters: Dict[str, str] = None
    ) -> List[LigBoxScore]:
        try:
            connection = db.get_connection()
            selected_columns = ", ".join(columns) if columns else "*"
            where_clauses = []
            params = []

            if filters:
                where_clauses = [f"{col} = %s" for col in filters.keys()]
                params.extend(filters.values())

            where_clause = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
            query = f"SELECT {selected_columns} FROM LIG_BOX_SCORE {where_clause} LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            cursor = connection.cursor()
            cursor.execute(query, params)
            box_scores = cursor.fetchall()

            if not box_scores:
                return []

            if columns:
                return [dict(zip(columns, box_score)) for box_score in box_scores]
            else:
                return [LigBoxScore(*box_score) for box_score in box_scores]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    @staticmethod
    def get_total_lig_box_scores(db: db, filters: Dict[str, str] = None) -> int:
        try:
            connection = db.get_connection()
            where_clauses = []
            params = []

            if filters:
                where_clauses = [f"{col} = %s" for col in filters.keys()]
                params.extend(filters.values())

            where_clause = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
            query = f"SELECT COUNT(*) FROM LIG_BOX_SCORE {where_clause}"
            cursor = connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result[0] if result else 0
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
