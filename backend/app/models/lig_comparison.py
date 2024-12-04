from dataclasses import dataclass
from datetime import datetime
from db.db import db
import mysql.connector

# game_id VARCHAR(50),
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
class Lig_Comparison:
    game_id: str
    game: str
    round_of_game: int
    phase: str
    season_team_id_a: str
    season_team_id_b: str
    fast_break_points_a: int
    fast_break_points_b: int
    turnover_points_a: int
    turnover_points_b: int
    second_chance_points_a: int
    second_chance_points_b: int
    defensive_rebounds_a: int
    offensive_rebounds_b: int
    offensive_rebounds_a: int
    defensive_rebounds_b: int
    turnovers_starters_a: int
    turnovers_bench_a: int
    turnovers_starters_b: int
    turnovers_bench_b: int
    steals_starters_a: int
    steals_bench_a: int
    steals_starters_b: int
    steals_bench_b: int
    assists_starters_a: int
    assists_bench_a: int
    assists_starters_b: int
    assists_bench_b: int
    points_starters_a: int
    points_bench_a: int
    points_starters_b: int
    points_bench_b: int
    max_lead_a: int
    max_lead_b: int
    minute_max_lead_a: int
    minute_max_lead_b: int
    points_max_lead_a: str
    points_max_lead_b: str

class Lig_ComparisonDAO():
    @staticmethod
    def create_lig_comparison(db: db, comparison: Lig_Comparison) -> None:
        try:
            connection  = db.get_connection()
            cursor = db.connection.cursor()
            query = """
                INSERT INTO LIG_COMPARISON (
                game_id,
                game,
                round_of_game,
                phase,
                season_team_id_a,
                season_team_id_b,
                fast_break_points_a,
                fast_break_points_b,
                turnover_points_a,
                turnover_points_b,
                second_chance_points_a,
                second_chance_points_b,
                defensive_rebounds_a,
                offensive_rebounds_b,
                offensive_rebounds_a,
                defensive_rebounds_b,
                turnovers_starters_a,
                turnovers_bench_a,
                turnovers_starters_b,
                turnovers_bench_b,
                steals_starters_a,
                steals_bench_a,
                steals_starters_b,
                steals_bench_b,
                assists_starters_a,
                assists_bench_a,
                assists_starters_b,
                assists_bench_b,
                points_starters_a,
                points_bench_a,
                points_starters_b,
                points_bench_b,
                max_lead_a,
                max_lead_b,
                minute_max_lead_a,
                minute_max_lead_b,
                points_max_lead_a,
                points_max_lead_b
                ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s
                )
                """
            cursor.execute(query, (
                comparison.game_id,
                comparison.game,
                comparison.round_of_game,
                comparison.phase,
                comparison.season_team_id_a,
                comparison.season_team_id_b,
                comparison.fast_break_points_a,
                comparison.fast_break_points_b,
                comparison.turnover_points_a,
                comparison.turnover_points_b,
                comparison.second_chance_points_a,
                comparison.second_chance_points_b,
                comparison.defensive_rebounds_a,
                comparison.offensive_rebounds_b,
                comparison.offensive_rebounds_a,
                comparison.defensive_rebounds_b,
                comparison.turnovers_starters_a,
                comparison.turnovers_bench_a,
                comparison.turnovers_starters_b,
                comparison.turnovers_bench_b,
                comparison.steals_starters_a,
                comparison.steals_bench_a,
                comparison.steals_starters_b,
                comparison.steals_bench_b,
                comparison.assists_starters_a,
                comparison.assists_bench_a,
                comparison.assists_starters_b,
                comparison.assists_bench_b,
                comparison.points_starters_a,
                comparison.points_bench_a,
                comparison.points_starters_b,
                comparison.points_bench_b,
                comparison.max_lead_a,
                comparison.max_lead_b,
                comparison.minute_max_lead_a,
                comparison.minute_max_lead_b,
                comparison.points_max_lead_a,
                comparison.points_max_lead_b
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
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
            query = """
            UPDATE LIG_COMPARISON SET
            game_id = %s,
            game = %s,
            round_of_game = %s,
            phase = %s,
            season_team_id_a = %s,
            season_team_id_b = %s,
            fast_break_points_a = %s,
            fast_break_points_b = %s,
            turnover_points_a = %s,
            turnover_points_b = %s,
            second_chance_points_a = %s,
            second_chance_points_b = %s,
            defensive_rebounds_a = %s,
            offensive_rebounds_b = %s,
            offensive_rebounds_a = %s,
            defensive_rebounds_b = %s,
            turnovers_starters_a = %s,
            turnovers_bench_a = %s,
            turnovers_starters_b = %s,
            turnovers_bench_b = %s,
            steals_starters_a = %s,
            steals_bench_a = %s,
            steals_starters_b = %s,
            steals_bench_b = %s,
            assists_starters_a = %s,
            assists_bench_a = %s,
            assists_starters_b = %s,
            assists_bench_b = %s,
            points_starters_a = %s,
            points_bench_a = %s,
            points_starters_b = %s,
            points_bench_b = %s,
            max_lead_a = %s,
            max_lead_b = %s,
            minute_max_lead_a = %s,
            minute_max_lead_b = %s,
            points_max_lead_a = %s,
            points_max_lead_b = %s
            WHERE game_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (
            comparison.game_id,
            comparison.game,
            comparison.round_of_game,
            comparison.phase,
            comparison.season_team_id_a,
            comparison.season_team_id_b,
            comparison.fast_break_points_a,
            comparison.fast_break_points_b,
            comparison.turnover_points_a,
            comparison.turnover_points_b,
            comparison.second_chance_points_a,
            comparison.second_chance_points_b,
            comparison.defensive_rebounds_a,
            comparison.offensive_rebounds_b,
            comparison.offensive_rebounds_a,
            comparison.defensive_rebounds_b,
            comparison.turnovers_starters_a,
            comparison.turnovers_bench_a,
            comparison.turnovers_starters_b,
            comparison.turnovers_bench_b,
            comparison.steals_starters_a,
            comparison.steals_bench_a,
            comparison.steals_starters_b,
            comparison.steals_bench_b,
            comparison.assists_starters_a,
            comparison.assists_bench_a,
            comparison.assists_starters_b,
            comparison.assists_bench_b,
            comparison.points_starters_a,
            comparison.points_bench_a,
            comparison.points_starters_b,
            comparison.points_bench_b,
            comparison.max_lead_a,
            comparison.max_lead_b,
            comparison.minute_max_lead_a,
            comparison.minute_max_lead_b,
            comparison.points_max_lead_a,
            comparison.points_max_lead_b,
            comparison.game_id  # The identifier in the WHERE clause
            ))
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