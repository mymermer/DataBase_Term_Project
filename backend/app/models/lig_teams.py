from dataclasses import dataclass
from datetime import datetime
from db.db import db
import mysql.connector

# season_team_id VARCHAR(50) PRIMARY KEY,
# games_played INT,
# minutes_played FLOAT,
# points INT,
# two_points_made INT,
# two_points_attempted INT,
# three_points_made INT,
# three_points_attempted INT,
# free_throws_made INT,
# free_throws_attempted INT,
# offensive_rebounds INT,
# defensive_rebounds INT,
# total_rebounds INT,
# assists INT,
# steals INT,
# turnovers INT,
# blocks_favour INT,
# blocks_against INT,
# fouls_committed INT,
# fouls_received INT,
# valuation INT,
# minutes_per_game FLOAT,
# points_per_game FLOAT,
# two_points_made_per_game FLOAT,
# two_points_attempted_per_game FLOAT,
# two_points_percentage FLOAT,
# three_points_made_per_game FLOAT,
# three_points_attempted_per_game FLOAT,
# three_points_percentage FLOAT,
# free_throws_made_per_game FLOAT,
# free_throws_attempted_per_game FLOAT,
# free_throws_percentage FLOAT,
# offensive_rebounds_per_game FLOAT,
# defensive_rebounds_per_game FLOAT,
# total_rebounds_per_game FLOAT,
# assists_per_game FLOAT,
# steals_per_game FLOAT,
# turnovers_per_game FLOAT,
# blocks_favour_per_game FLOAT,
# blocks_against_per_game FLOAT,
# fouls_committed_per_game FLOAT,
# fouls_received_per_game FLOAT,
# valuation_per_game FLOAT

@dataclass
class Lig_Teams:
    season_team_id: str
    games_played: int
    minutes_played: float
    points: int
    two_points_made: int
    two_points_attempted: int
    three_points_made: int
    three_points_attempted: int
    free_throws_made: int
    free_throws_attempted: int
    offensive_rebounds: int
    defensive_rebounds: int
    total_rebounds: int
    assists: int
    steals: int
    turnovers: int
    blocks_favour: int
    blocks_against: int
    fouls_committed: int
    fouls_received: int
    valuation: int
    minutes_per_game: float
    points_per_game: float
    two_points_made_per_game: float
    two_points_attempted_per_game: float
    two_points_percentage: float
    three_points_made_per_game: float
    three_points_attempted_per_game: float
    three_points_percentage: float
    free_throws_made_per_game: float
    free_throws_attempted_per_game: float
    free_throws_percentage: float
    offensive_rebounds_per_game: float
    defensive_rebounds_per_game: float
    total_rebounds_per_game: float
    assists_per_game: float
    steals_per_game: float
    turnovers_per_game: float
    blocks_favour_per_game: float
    blocks_against_per_game: float
    fouls_committed_per_game: float
    fouls_received_per_game: float
    valuation_per_game: float

class Lig_TeamsDAO():
    @staticmethod
    def create_lig_teams(db: db, team: Lig_Teams) -> None:
        try:
            connection  = db.get_connection()
            cursor = db.connection.cursor()
            query = """
                INSERT INTO LIG_TEAMS (
                season_team_id,
                games_played,
                minutes_played,
                points,
                two_points_made,
                two_points_attempted,
                three_points_made,
                three_points_attempted,
                free_throws_made,
                free_throws_attempted,
                offensive_rebounds,
                defensive_rebounds,
                total_rebounds,
                assists,
                steals,
                turnovers,
                blocks_favour,
                blocks_against,
                fouls_committed,
                fouls_received,
                valuation,
                minutes_per_game,
                points_per_game,
                two_points_made_per_game,
                two_points_attempted_per_game,
                two_points_percentage,
                three_points_made_per_game,
                three_points_attempted_per_game,
                three_points_percentage,
                free_throws_made_per_game,
                free_throws_attempted_per_game,
                free_throws_percentage,
                offensive_rebounds_per_game,
                defensive_rebounds_per_game,
                total_rebounds_per_game,
                assists_per_game,
                steals_per_game,
                turnovers_per_game,
                blocks_favour_per_game,
                blocks_against_per_game,
                fouls_committed_per_game,
                fouls_received_per_game,
                valuation_per_game
                ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s
                )
                """

            cursor.execute(query, (
                team.season_team_id,
                team.games_played,
                team.minutes_played,
                team.points,
                team.two_points_made,
                team.two_points_attempted,
                team.three_points_made,
                team.three_points_attempted,
                team.free_throws_made,
                team.free_throws_attempted,
                team.offensive_rebounds,
                team.defensive_rebounds,
                team.total_rebounds,
                team.assists,
                team.steals,
                team.turnovers,
                team.blocks_favour,
                team.blocks_against,
                team.fouls_committed,
                team.fouls_received,
                team.valuation,
                team.minutes_per_game,
                team.points_per_game,
                team.two_points_made_per_game,
                team.two_points_attempted_per_game,
                team.two_points_percentage,
                team.three_points_made_per_game,
                team.three_points_attempted_per_game,
                team.three_points_percentage,
                team.free_throws_made_per_game,
                team.free_throws_attempted_per_game,
                team.free_throws_percentage,
                team.offensive_rebounds_per_game,
                team.defensive_rebounds_per_game,
                team.total_rebounds_per_game,
                team.assists_per_game,
                team.steals_per_game,
                team.turnovers_per_game,
                team.blocks_favour_per_game,
                team.blocks_against_per_game,
                team.fouls_committed_per_game,
                team.fouls_received_per_game,
                team.valuation_per_game
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_lig_teams(db: db, season_team_id: str) -> Lig_Teams:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM LIG_TEAMS WHERE season_team_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (season_team_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return Lig_Teams(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_all_lig_teams(db: db) -> list:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM LIG_TEAMS
            """
            cursor = connection.cursor()
            cursor.execute(query)
            teams = cursor.fetchall()
            if teams is None:
                return None
            #! special return might not be needed but we will see
            return [Lig_Teams(*team) for team in teams]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()  
    
    
    @staticmethod
    def update_lig_teams(db: db, team: Lig_Teams) -> None:
        try:
            connection = db.get_connection()
            query = """
            UPDATE LIG_TEAMS SET
            season_team_id = %s,
            games_played = %s,
            minutes_played = %s,
            points = %s,
            two_points_made = %s,
            two_points_attempted = %s,
            three_points_made = %s,
            three_points_attempted = %s,
            free_throws_made = %s,
            free_throws_attempted = %s,
            offensive_rebounds = %s,
            defensive_rebounds = %s,
            total_rebounds = %s,
            assists = %s,
            steals = %s,
            turnovers = %s,
            blocks_favour = %s,
            blocks_against = %s,
            fouls_committed = %s,
            fouls_received = %s,
            valuation = %s,
            minutes_per_game = %s,
            points_per_game = %s,
            two_points_made_per_game = %s,
            two_points_attempted_per_game = %s,
            two_points_percentage = %s,
            three_points_made_per_game = %s,
            three_points_attempted_per_game = %s,
            three_points_percentage = %s,
            free_throws_made_per_game = %s,
            free_throws_attempted_per_game = %s,
            free_throws_percentage = %s,
            offensive_rebounds_per_game = %s,
            defensive_rebounds_per_game = %s,
            total_rebounds_per_game = %s,
            assists_per_game = %s,
            steals_per_game = %s,
            turnovers_per_game = %s,
            blocks_favour_per_game = %s,
            blocks_against_per_game = %s,
            fouls_committed_per_game = %s,
            fouls_received_per_game = %s,
            valuation_per_game = %s
            WHERE season_team_id = %s
            """

            cursor = connection.cursor()
            cursor.execute(query, (
            team.season_team_id,
            team.games_played,
            team.minutes_played,
            team.points,
            team.two_points_made,
            team.two_points_attempted,
            team.three_points_made,
            team.three_points_attempted,
            team.free_throws_made,
            team.free_throws_attempted,
            team.offensive_rebounds,
            team.defensive_rebounds,
            team.total_rebounds,
            team.assists,
            team.steals,
            team.turnovers,
            team.blocks_favour,
            team.blocks_against,
            team.fouls_committed,
            team.fouls_received,
            team.valuation,
            team.minutes_per_game,
            team.points_per_game,
            team.two_points_made_per_game,
            team.two_points_attempted_per_game,
            team.two_points_percentage,
            team.three_points_made_per_game,
            team.three_points_attempted_per_game,
            team.three_points_percentage,
            team.free_throws_made_per_game,
            team.free_throws_attempted_per_game,
            team.free_throws_percentage,
            team.offensive_rebounds_per_game,
            team.defensive_rebounds_per_game,
            team.total_rebounds_per_game,
            team.assists_per_game,
            team.steals_per_game,
            team.turnovers_per_game,
            team.blocks_favour_per_game,
            team.blocks_against_per_game,
            team.fouls_committed_per_game,
            team.fouls_received_per_game,
            team.valuation_per_game,
            team.season_team_id  # The identifier in the WHERE clause
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_lig_teams(db: db, season_team_id: str) -> None:
        try:
            connection = db.get_connection()
            query = """
                DELETE FROM LIG_TEAMS WHERE season_team_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (season_team_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()