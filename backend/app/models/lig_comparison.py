from dataclasses import dataclass
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
# minute_max_lead_b INT

@dataclass
class Lig_Comparison:
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

class Lig_ComparisonDAO():
    @staticmethod
    def create_lig_comparison(db: db, comparison: Lig_Comparison) -> None:
        """
        Insert a new LIG_COMPARISON record with only provided columns.

        Args:
            db: Database connection.
            comparison: A `Lig_Comparison` object or dictionary containing column-value pairs for the record.
        """
        try:
            connection  = db.get_connection()
            cursor = connection.cursor()

            # Convert Lig_Comparison object to dictionary if necessary
            if isinstance(comparison, Lig_Comparison):
                comparison = comparison.__dict__

            # Dynamically construct query based on provided keys
            columns = ", ".join(comparison.keys())
            placeholders = ", ".join(["%s"] * len(comparison))
            query = f"INSERT INTO LIG_COMPARISON ({columns}) VALUES ({placeholders})"

            # Execute query with provided values
            cursor.execute(query, list(comparison.values()))
            connection.commit()

            print(f"Successfully created LIG_COMPARISON with provided data.")

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
    def get_lig_comparison(db: db, game_id: str) -> Lig_Comparison:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM LIG_COMPARISON WHERE game_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return Lig_Comparison(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_all_lig_comparisons(db: db) -> list:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM LIG_COMPARISON
            """
            cursor = connection.cursor()
            cursor.execute(query)
            comparisons = cursor.fetchall()
            if comparisons is None:
                return None
            #! special return might not be needed but we will see
            return [Lig_Comparison(*comparison) for comparison in comparisons]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()  
    
    
    @staticmethod
    def update_lig_comparison(db: db, comparison: Lig_Comparison) -> None:
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

            # Construct dynamic SQL query
            if not fields_to_update:
                raise ValueError("No fields to update were provided.")
            
            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"""
            UPDATE LIG_COMPARISON
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
    def delete_lig_comparison(db: db, game_id: str) -> None:
        try:
            connection = db.get_connection()
            query = """
                DELETE FROM LIG_COMPARISON WHERE game_id = %s
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
    def get_paginated_lig_comparison(db: db, offset: int = 0, limit: int = 25, columns: list = None, filters: dict = None, sort_by: str = None, order: str = 'asc') -> list:
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
                SELECT {selected_columns} FROM LIG_COMPARISON
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

            # Map fetched rows to Lig_Comparison objects or dicts
            if columns:
                return [dict(zip(columns, comparison)) for comparison in comparisons]
            else:
                return [Lig_Comparison(*comparison) for comparison in comparisons]
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_total_lig_comparison(db: db, filters: dict = None) -> int:
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
                SELECT COUNT(*) FROM LIG_COMPARISON
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
    def get_paginated_lig_comparison_with_like(
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
                SELECT {selected_columns} FROM LIG_COMPARISON
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

            # Map fetched rows to dicts or raw objects
            if columns:
                return [dict(zip(columns, comparison)) for comparison in comparisons]
            else:
                return [Lig_Comparison(*comparison) for comparison in comparisons]

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
                SELECT DISTINCT {selected_columns} FROM LIG_COMPARISON
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

    # For the join operation
    @staticmethod
    def get_win_loss_history(db: db, team1: str, team2: str) -> dict:
        try:
            connection = db.get_connection()

            # Fetch the abbreviations for the teams from `teams`
            fetch_abbr_query = """
                SELECT abbreviation, full_name
                FROM teams
                WHERE full_name IN (%s, %s);
            """
            cursor = connection.cursor(dictionary=True)
            cursor.execute(fetch_abbr_query, [team1, team2])
            abbr_results = cursor.fetchall()

            # Check if abbreviations are found for both teams
            if len(abbr_results) != 2:
                print("Error: Abbreviations for one or both teams not found.")
                return {
                    "error": "Abbreviations for one or both teams not found.",
                    "total_games": 0,
                    "team1_wins": 0,
                    "team2_wins": 0,
                    "history": []
                }

            # Map abbreviations to their corresponding teams
            abbr_map = {row["full_name"]: row["abbreviation"] for row in abbr_results}
            abbr_team1 = abbr_map.get(team1)
            abbr_team2 = abbr_map.get(team2)

            if not abbr_team1 or not abbr_team2:
                print("Error: Abbreviations mapping failed.")
                return {
                    "error": "Abbreviations mapping failed.",
                    "total_games": 0,
                    "team1_wins": 0,
                    "team2_wins": 0,
                    "history": []
                }

            # Format the game strings
            game1 = f"{abbr_team1}-{abbr_team2}"
            game2 = f"{abbr_team2}-{abbr_team1}"

            # Query to fetch game history with join between LIG_HEADER and LIG_COMPARISON
            game_history_query = """
                SELECT 
                    c.game_id,
                    c.game,
                    h.date_of_game,
                    h.time_of_game,
                    h.score_a,
                    h.score_b,
                    h.winner
                FROM 
                    LIG_COMPARISON c
                JOIN 
                    LIG_HEADER h
                ON 
                    c.game_id = h.game_id
                WHERE 
                    c.game IN (%s, %s)
                ORDER BY 
                    h.date_of_game ASC;
            """
            cursor.execute(game_history_query, [game1, game2])
            game_results = cursor.fetchall()

            # Calculate win-loss and draw counts
            team1_wins = 0
            team2_wins = 0
            draws = 0

            for game in game_results:
                if game["score_a"] > game["score_b"]:  # Check if team_a wins
                    if game["game"].startswith(abbr_team1):
                        team1_wins += 1
                    else:
                        team2_wins += 1
                elif game["score_b"] > game["score_a"]:  # Check if team_b wins
                    if game["game"].startswith(abbr_team1):
                        team2_wins += 1
                    else:
                        team1_wins += 1
                else:  # Draw case
                    draws += 1

            total_games = len(game_results)

            return {
            "total_games": total_games,
            "team1_wins": team1_wins,
            "team2_wins": team2_wins,
            "draws": draws,
            "history": game_results
            }
        
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            raise
        finally:
            cursor.close()
            connection.close()