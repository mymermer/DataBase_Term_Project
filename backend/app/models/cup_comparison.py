from dataclasses import dataclass
from datetime import datetime
from app.db.db import db
import mysql.connector
from typing import Optional

# game_id VARCHAR(50) PRIMARY KEY,
# game VARCHAR(50),
# round_of_game INT,
# phase VARCHAR(50),
# season_team_id_a VARCHAR(50),
# season_team_id_b VARCHAR(50),
# fast_break_points_a INT,
# fast_break_points_b INT,
# turnover_points_a INT,
# turnover_points_b INT,
# second_chance_points_a INT,
# second_chance_points_b INT,
# defensive_rebounds_a INT,
# offensive_rebounds_b INT,
# offensive_rebounds_a INT,
# defensive_rebounds_b INT,
# turnovers_starters_a INT,
# turnovers_bench_a INT,
# turnovers_starters_b INT,
# turnovers_bench_b INT,
# steals_starters_a INT,
# steals_bench_a INT,
# steals_starters_b INT,
# steals_bench_b INT,
# assists_starters_a INT,
# assists_bench_a INT,
# assists_starters_b INT,
# assists_bench_b INT,
# points_starters_a INT,
# points_bench_a INT,
# points_starters_b INT,
# points_bench_b INT,
# max_lead_a INT,
# max_lead_b INT,
# minute_max_lead_a INT,
# minute_max_lead_b INT,
# points_max_lead_a VARCHAR(50),
# points_max_lead_b VARCHAR(50)

@dataclass
class Cup_Comparison:
    game_id: Optional[str] = None
    game: Optional[str] = None
    round_of_game: Optional[int] = None
    phase: Optional[str] = None
    season_team_id_a: Optional[str] = None
    season_team_id_b: Optional[str] = None
    fast_break_points_a: Optional[int] = None
    fast_break_points_b: Optional[int] = None
    turnover_points_a: Optional[int] = None
    turnover_points_b: Optional[int] = None
    second_chance_points_a: Optional[int] = None
    second_chance_points_b: Optional[int] = None
    defensive_rebounds_a: Optional[int] = None
    offensive_rebounds_b: Optional[int] = None
    offensive_rebounds_a: Optional[int] = None
    defensive_rebounds_b: Optional[int] = None
    turnovers_starters_a: Optional[int] = None
    turnovers_bench_a: Optional[int] = None
    turnovers_starters_b: Optional[int] = None
    turnovers_bench_b: Optional[int] = None
    steals_starters_a: Optional[int] = None
    steals_bench_a: Optional[int] = None
    steals_starters_b: Optional[int] = None
    steals_bench_b: Optional[int] = None
    assists_starters_a: Optional[int] = None
    assists_bench_a: Optional[int] = None
    assists_starters_b: Optional[int] = None
    assists_bench_b: Optional[int] = None
    points_starters_a: Optional[int] = None
    points_bench_a: Optional[int] = None
    points_starters_b: Optional[int] = None
    points_bench_b: Optional[int] = None
    max_lead_a: Optional[int] = None
    max_lead_b: Optional[int] = None
    minute_max_lead_a: Optional[int] = None
    minute_max_lead_b: Optional[int] = None
    points_max_lead_a: Optional[str] = None
    points_max_lead_b: Optional[str] = None


class Cup_ComparisonDAO():
    @staticmethod
    def create_cup_comparison(db: db, comparison: Cup_Comparison) -> None:
        """
        Insert a new CUP_COMPARISON record with only provided columns.

        Args:
            db: Database connection.
            comparison: A `Cup_Comparison` object or dictionary containing column-value pairs for the record.
        """
        try:
            connection  = db.get_connection()
            cursor = db.connection.cursor()

            # Convert Cup_Comparison object to dictionary if necessary
            if isinstance(comparison, Cup_Comparison):
                comparison = comparison.__dict__

            # Dynamically construct query based on provided keys
            columns = ", ".join(comparison.keys())
            placeholders = ", ".join(["%s"] * len(comparison))
            query = f"INSERT INTO CUP_COMPARISON ({columns}) VALUES ({placeholders})"

            # Execute query with provided values
            cursor.execute(query, list(comparison.values()))
            connection.commit()

            print(f"Successfully created CUP_COMPARISON with provided data.")

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
    def get_cup_comparison(db: db, game_id: str) -> Cup_Comparison:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM CUP_COMPARISON WHERE game_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return Cup_Comparison(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_all_cup_comparisons(db: db) -> list:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM CUP_COMPARISON
            """
            cursor = connection.cursor()
            cursor.execute(query)
            comparisons = cursor.fetchall()
            if comparisons is None:
                return None
            #! special return might not be needed but we will see
            return [Cup_Comparison(*comparison) for comparison in comparisons]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()  
    
    
    @staticmethod
    def update_cup_comparison(db: db, comparison: Cup_Comparison) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            # Extract fields from the "comparison" object
            fields_to_update = {}
            if comparison.game_id is not None:
                fields_to_update['game_id'] = comparison.game_id
            if comparison.game is not None:
                fields_to_update['game'] = comparison.game
            if comparison.round_of_game is not None:
                fields_to_update['round_of_game'] = comparison.round_of_game
            if comparison.phase is not None:
                fields_to_update['phase'] = comparison.phase
            if comparison.season_team_id_a is not None:
                fields_to_update['season_team_id_a'] = comparison.season_team_id_a
            if comparison.season_team_id_b is not None:
                fields_to_update['season_team_id_b'] = comparison.season_team_id_b
            if comparison.fast_break_points_a is not None:
                fields_to_update['fast_break_points_a'] = comparison.fast_break_points_a
            if comparison.fast_break_points_b is not None:
                fields_to_update['fast_break_points_b'] = comparison.fast_break_points_b
            if comparison.turnover_points_a is not None:
                fields_to_update['turnover_points_a'] = comparison.turnover_points_a
            if comparison.turnover_points_b is not None:
                fields_to_update['turnover_points_b'] = comparison.turnover_points_b
            if comparison.second_chance_points_a is not None:
                fields_to_update['second_chance_points_a'] = comparison.second_chance_points_a
            if comparison.second_chance_points_b is not None:
                fields_to_update['second_chance_points_b'] = comparison.second_chance_points_b
            if comparison.defensive_rebounds_a is not None:
                fields_to_update['defensive_rebounds_a'] = comparison.defensive_rebounds_a
            if comparison.offensive_rebounds_b is not None:
                fields_to_update['offensive_rebounds_b'] = comparison.offensive_rebounds_b
            if comparison.offensive_rebounds_a is not None:
                fields_to_update['offensive_rebounds_a'] = comparison.offensive_rebounds_a
            if comparison.defensive_rebounds_b is not None:
                fields_to_update['defensive_rebounds_b'] = comparison.defensive_rebounds_b
            if comparison.turnovers_starters_a is not None:
                fields_to_update['turnovers_starters_a'] = comparison.turnovers_starters_a
            if comparison.turnovers_bench_a is not None:
                fields_to_update['turnovers_bench_a'] = comparison.turnovers_bench_a
            if comparison.turnovers_starters_b is not None:
                fields_to_update['turnovers_starters_b'] = comparison.turnovers_starters_b
            if comparison.turnovers_bench_b is not None:
                fields_to_update['turnovers_bench_b'] = comparison.turnovers_bench_b
            if comparison.steals_starters_a is not None:
                fields_to_update['steals_starters_a'] = comparison.steals_starters_a
            if comparison.steals_bench_a is not None:
                fields_to_update['steals_bench_a'] = comparison.steals_bench_a
            if comparison.steals_starters_b is not None:
                fields_to_update['steals_starters_b'] = comparison.steals_starters_b
            if comparison.steals_bench_b is not None:
                fields_to_update['steals_bench_b'] = comparison.steals_bench_b
            if comparison.assists_starters_a is not None:
                fields_to_update['assists_starters_a'] = comparison.assists_starters_a
            if comparison.assists_bench_a is not None:
                fields_to_update['assists_bench_a'] = comparison.assists_bench_a
            if comparison.assists_starters_b is not None:
                fields_to_update['assists_starters_b'] = comparison.assists_starters_b
            if comparison.assists_bench_b is not None:
                fields_to_update['assists_bench_b'] = comparison.assists_bench_b
            if comparison.points_starters_a is not None:
                fields_to_update['points_starters_a'] = comparison.points_starters_a
            if comparison.points_bench_a is not None:
                fields_to_update['points_bench_a'] = comparison.points_bench_a
            if comparison.points_starters_b is not None:
                fields_to_update['points_starters_b'] = comparison.points_starters_b
            if comparison.points_bench_b is not None:
                fields_to_update['points_bench_b'] = comparison.points_bench_b
            if comparison.max_lead_a is not None:
                fields_to_update['max_lead_a'] = comparison.max_lead_a
            if comparison.max_lead_b is not None:
                fields_to_update['max_lead_b'] = comparison.max_lead_b
            if comparison.minute_max_lead_a is not None:
                fields_to_update['minute_max_lead_a'] = comparison.minute_max_lead_a
            if comparison.minute_max_lead_b is not None:
                fields_to_update['minute_max_lead_b'] = comparison.minute_max_lead_b
            if comparison.points_max_lead_a is not None:
                fields_to_update['points_max_lead_a'] = comparison.points_max_lead_a
            if comparison.points_max_lead_b is not None:
                fields_to_update['points_max_lead_b'] = comparison.points_max_lead_b

            # Construct dynamic SQL query
            if not fields_to_update:
                raise ValueError("No fields to update were provided.")
            
            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"""
            UPDATE CUP_COMPARISON
            SET {set_clause}
            WHERE game_id = %s
            """
            # Prepare values for the query
            values = list(fields_to_update.values())
            values.append(comparison.game_id)  # Add identifier for WHERE clause

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
    def delete_cup_comparison(db: db, game_id: str) -> None:
        try:
            connection = db.get_connection()
            query = """
                DELETE FROM CUP_COMPARISON WHERE game_id = %s
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
    def get_paginated_cup_comparison(db: db, offset: int = 0, limit: int = 25, columns: list = None, filters: dict = None, sort_by: str = None, order: str = 'asc') -> list:
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
                SELECT {selected_columns} FROM CUP_COMPARISON
                {where_clause}
                {order_clause}
                LIMIT %s OFFSET %s
            """
            
            # Append limit and offset to the params
            params.extend([limit, offset])
            
            cursor = connection.cursor()
            cursor.execute(query, params)
            comparisons = cursor.fetchall()

            if comparisons is None:
                return None

            # Map fetched rows to Cup_Comparison objects or dicts
            if columns:
                return [dict(zip(columns, comparison)) for comparison in comparisons]
            else:
                return [Cup_Comparison(*comparison) for comparison in comparisons]
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_total_cup_comparison(db: db, filters: dict = None) -> int:
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
                SELECT COUNT(*) FROM CUP_COMPARISON
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