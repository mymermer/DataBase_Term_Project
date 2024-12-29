from dataclasses import dataclass
from app.db.db import db
import mysql.connector
from typing import Optional

@dataclass
class Cup_Header:
    game_id: Optional[str] = None
    game: Optional[str] = None
    date_of_game: Optional[str] = None
    time_of_game: Optional[str] = None
    round_of_game: Optional[int] = None
    phase: Optional[str] = None
    season_team_id_a: Optional[str] = None
    season_team_id_b: Optional[str] = None
    score_a: Optional[int] = None
    score_b: Optional[int] = None
    coach_a: Optional[str] = None
    coach_b: Optional[str] = None
    game_time: Optional[str] = None
    referee_1: Optional[str] = None
    referee_2: Optional[str] = None
    referee_3: Optional[str] = None
    stadium: Optional[str] = None
    capacity: Optional[int] = None
    fouls_a: Optional[int] = None
    fouls_b: Optional[int] = None
    timeouts_a: Optional[int] = None
    timeouts_b: Optional[int] = None
    score_quarter_1_a: Optional[int] = None
    score_quarter_2_a: Optional[int] = None
    score_quarter_3_a: Optional[int] = None
    score_quarter_4_a: Optional[int] = None
    score_quarter_1_b: Optional[int] = None
    score_quarter_2_b: Optional[int] = None
    score_quarter_3_b: Optional[int] = None
    score_quarter_4_b: Optional[int] = None
    score_extra_time_1_a: Optional[int] = None
    score_extra_time_2_a: Optional[int] = None
    score_extra_time_3_a: Optional[int] = None
    score_extra_time_4_a: Optional[int] = None
    score_extra_time_1_b: Optional[int] = None
    score_extra_time_2_b: Optional[int] = None
    score_extra_time_3_b: Optional[int] = None
    score_extra_time_4_b: Optional[int] = None
    winner: Optional[str] = None

class Cup_HeaderDAO():
    @staticmethod
    def create_cup_header(db: db, header: Cup_Header) -> None:
        """
        Insert a new CUP_HEADER record with only provided columns.

        Args:
            db: Database connection.
            header: A `Cup_Header` object or dictionary containing column-value pairs for the record.
        """
        try:
            connection  = db.get_connection()
            cursor = connection.cursor()

            # Convert Cup_Header object to dictionary if necessary
            if isinstance(header, Cup_Header):
                header = header.__dict__

            # Dynamically construct query based on provided keys
            columns = ", ".join(header.keys())
            placeholders = ", ".join(["%s"] * len(header))
            query = f"INSERT INTO CUP_HEADER ({columns}) VALUES ({placeholders})"

            # Execute query with provided values
            cursor.execute(query, list(header.values()))
            connection.commit()

            print(f"Successfully created CUP_HEADER with provided data.")

        except mysql.connector.Error as error:
            print(f"Database Error: {error}")
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
    def get_cup_header(db: db, game_id: str) -> Cup_Header:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM CUP_HEADER WHERE game_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return Cup_Header(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_all_cup_headers(db: db) -> list:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM CUP_HEADER
            """
            cursor = connection.cursor()
            cursor.execute(query)
            headers = cursor.fetchall()
            if headers is None:
                return None
            #! special return might not be needed but we will see
            return [Cup_Header(*header) for header in headers]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()  
    
    
    @staticmethod
    def update_cup_header(db: db, header: Cup_Header) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            # Extract fields from the "header" object
            fields_to_update = {}
            if header.game_id is not None:
                fields_to_update['game_id'] = header.game_id
            if header.game is not None:
                fields_to_update['game'] = header.game
            if header.date_of_game is not None:
                fields_to_update['date_of_game'] = header.date_of_game
            if header.time_of_game is not None:
                fields_to_update['time_of_game'] = header.time_of_game
            if header.round_of_game is not None:
                fields_to_update['round_of_game'] = header.round_of_game
            if header.phase is not None:
                fields_to_update['phase'] = header.phase
            if header.season_team_id_a is not None:
                fields_to_update['season_team_id_a'] = header.season_team_id_a
            if header.season_team_id_b is not None:
                fields_to_update['season_team_id_b'] = header.season_team_id_b
            if header.score_a is not None:
                fields_to_update['score_a'] = header.score_a
            if header.score_b is not None:
                fields_to_update['score_b'] = header.score_b
            if header.coach_a is not None:
                fields_to_update['coach_a'] = header.coach_a
            if header.coach_b is not None:
                fields_to_update['coach_b'] = header.coach_b
            if header.game_time is not None:
                fields_to_update['game_time'] = header.game_time
            if header.referee_1 is not None:
                fields_to_update['referee_1'] = header.referee_1
            if header.referee_2 is not None:
                fields_to_update['referee_2'] = header.referee_2
            if header.referee_3 is not None:
                fields_to_update['referee_3'] = header.referee_3
            if header.stadium is not None:
                fields_to_update['stadium'] = header.stadium
            if header.capacity is not None:
                fields_to_update['capacity'] = header.capacity
            if header.fouls_a is not None:
                fields_to_update['fouls_a'] = header.fouls_a
            if header.fouls_b is not None:
                fields_to_update['fouls_b'] = header.fouls_b
            if header.timeouts_a is not None:
                fields_to_update['timeouts_a'] = header.timeouts_a
            if header.timeouts_b is not None:
                fields_to_update['timeouts_b'] = header.timeouts_b
            if header.score_quarter_1_a is not None:
                fields_to_update['score_quarter_1_a'] = header.score_quarter_1_a
            if header.score_quarter_2_a is not None:
                fields_to_update['score_quarter_2_a'] = header.score_quarter_2_a
            if header.score_quarter_3_a is not None:
                fields_to_update['score_quarter_3_a'] = header.score_quarter_3_a
            if header.score_quarter_4_a is not None:
                fields_to_update['score_quarter_4_a'] = header.score_quarter_4_a
            if header.score_quarter_1_b is not None:
                fields_to_update['score_quarter_1_b'] = header.score_quarter_1_b
            if header.score_quarter_2_b is not None:
                fields_to_update['score_quarter_2_b'] = header.score_quarter_2_b
            if header.score_quarter_3_b is not None:
                fields_to_update['score_quarter_3_b'] = header.score_quarter_3_b
            if header.score_quarter_4_b is not None:
                fields_to_update['score_quarter_4_b'] = header.score_quarter_4_b
            if header.score_extra_time_1_a is not None:
                fields_to_update['score_extra_time_1_a'] = header.score_extra_time_1_a
            if header.score_extra_time_2_a is not None:
                fields_to_update['score_extra_time_2_a'] = header.score_extra_time_2_a
            if header.score_extra_time_3_a is not None:
                fields_to_update['score_extra_time_3_a'] = header.score_extra_time_3_a
            if header.score_extra_time_4_a is not None:
                fields_to_update['score_extra_time_4_a'] = header.score_extra_time_4_a
            if header.score_extra_time_1_b is not None:
                fields_to_update['score_extra_time_1_b'] = header.score_extra_time_1_b
            if header.score_extra_time_2_b is not None:
                fields_to_update['score_extra_time_2_b'] = header.score_extra_time_2_b
            if header.score_extra_time_3_b is not None:
                fields_to_update['score_extra_time_3_b'] = header.score_extra_time_3_b
            if header.score_extra_time_4_b is not None:
                fields_to_update['score_extra_time_4_b'] = header.score_extra_time_4_b
            if header.winner is not None:
                fields_to_update['winner'] = header.winner

            # Construct dynamic SQL query
            if not fields_to_update:
                raise ValueError("No fields to update were provided.")
            
            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"""
            UPDATE CUP_HEADER
            SET {set_clause}
            WHERE game_id = %s
            """
            # Prepare values for the query
            values = list(fields_to_update.values())
            values.append(header.game_id)  # Add identifier for WHERE clause

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
    def delete_cup_header(db: db, game_id: str) -> None:
        try:
            connection = db.get_connection()
            query = """
                DELETE FROM CUP_HEADER WHERE game_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_paginated_cup_header(db: db, offset: int = 0, limit: int = 25, columns: list = None, filters: dict = None, sort_by: str = None, order: str = 'asc') -> list:
        try:
            connection = db.get_connection()
            
            # Build the SELECT part of the query
            selected_columns = ", ".join(columns) if columns else "*"

            # Build the WHERE clause dynamically based on filters
            where_clauses = []
            params = []
            if filters:
                for column, value in filters.items():
                    where_clauses.append(f"{column} = %s")
                    params.append(value)

            where_clause = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

            # Add ORDER BY clause
            order_clause = ""
            if sort_by:
                if order.lower() not in ['asc', 'desc']:
                    order = 'asc'  # Default to ascending
                order_clause = f"ORDER BY {sort_by} {order.upper()}"

            # Final query with LIMIT and OFFSET
            query = f"""
                SELECT {selected_columns} FROM CUP_HEADER
                {where_clause}
                {order_clause}
                LIMIT %s OFFSET %s
            """
            
            # Append limit and offset to the params
            params.extend([limit, offset])
            
            cursor = connection.cursor()
            cursor.execute(query, params)
            headers = cursor.fetchall()

            if headers is None:
                return None

            # Map fetched rows to Cup_Header objects or dicts
            if columns:
                return [dict(zip(columns, header)) for header in headers]
            else:
                return [Cup_Header(*header) for header in headers]
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_total_cup_header(db: db, filters: dict = None) -> int:
        try:
            connection = db.get_connection()

            # Build the WHERE clause dynamically based on filters
            where_clauses = []
            params = []
            if filters:
                for column, value in filters.items():
                    where_clauses.append(f"{column} = %s")  # Use %s as a placeholder
                    params.append(value)

            where_clause = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
            
            query = f"""
                SELECT COUNT(*) FROM CUP_HEADER
                {where_clause}
            """
            cursor = connection.cursor()
            cursor.execute(query, params)  # Pass params for the placeholders
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

    @staticmethod
    def get_paginated_cup_header_with_like(
        db: db,
        like_pattern: str,
        offset: int = 0,
        limit: int = 25,
        columns: list = None,
        filters: dict = None,
        sort_by: str = None,
        order: str = 'asc'
    ) -> list:
        
        try:
            connection = db.get_connection()

            # Add `%` wildcard to the LIKE pattern
            like_pattern = f"{like_pattern}%"

            # Build the SELECT part of the query
            selected_columns = ", ".join(columns) if columns else "*"

            # Build the WHERE clause dynamically based on filters
            where_clauses = [f"game_id LIKE %s"]
            params = [like_pattern]

            if filters:
                for column, value in filters.items():
                    where_clauses.append(f"{column} = %s")
                    params.append(value)

            where_clause = f"WHERE {' AND '.join(where_clauses)}"

            # Add ORDER BY clause
            order_clause = ""
            if sort_by:
                if order.lower() not in ['asc', 'desc']:
                    order = 'asc'  # Default to ascending
                order_clause = f"ORDER BY {sort_by} {order.upper()}"

            # Final query with LIMIT and OFFSET
            query = f"""
                SELECT {selected_columns} FROM CUP_HEADER
                {where_clause}
                {order_clause}
                LIMIT %s OFFSET %s
            """
            
            # Append limit and offset to the params
            params.extend([limit, offset])
            
            cursor = connection.cursor()
            cursor.execute(query, params)
            headers = cursor.fetchall()

            if headers is None:
                return None

            # Map fetched rows to dicts or raw objects
            if columns:
                return [dict(zip(columns, header)) for header in headers]
            else:
                return [Cup_Header(*header) for header in headers]

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_distinct_games_with_like(
        db: db,
        like_pattern: str,
        columns: list = None
    ) -> list:

        try:
            connection = db.get_connection()

            # Add `%` wildcard to the LIKE pattern
            like_pattern = f"{like_pattern}%"

            # Default columns to return
            selected_columns = ", ".join(columns) if columns else "game"

            # WHERE clause for the LIKE filter
            where_clause = "WHERE game_id LIKE %s"
            params = [like_pattern]

            # Query to fetch distinct games
            query = f"""
                SELECT DISTINCT {selected_columns} FROM CUP_HEADER
                {where_clause}
            """

            cursor = connection.cursor()
            cursor.execute(query, params)
            distinct_games = cursor.fetchall()

            if distinct_games is None:
                return None

            # Map fetched rows to dicts or raw values if only one column is selected
            if columns:
                return [dict(zip(columns, row)) for row in distinct_games]
            else:
                return [row[0] for row in distinct_games]  # Only return 'game' column

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise
        finally:
            cursor.close()
            connection.close()