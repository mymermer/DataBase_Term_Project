from dataclasses import dataclass
from datetime import datetime
from app.db.db import db
import mysql.connector
from typing import Optional

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
    season_team_id: Optional[str] = None
    games_played: Optional[int] = None
    minutes_played: Optional[float] = None
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
    minutes_per_game: Optional[float] = None
    points_per_game: Optional[float] = None
    two_points_made_per_game: Optional[float] = None
    two_points_attempted_per_game: Optional[float] = None
    two_points_percentage: Optional[float] = None
    three_points_made_per_game: Optional[float] = None
    three_points_attempted_per_game: Optional[float] = None
    three_points_percentage: Optional[float] = None
    free_throws_made_per_game: Optional[float] = None
    free_throws_attempted_per_game: Optional[float] = None
    free_throws_percentage: Optional[float] = None
    offensive_rebounds_per_game: Optional[float] = None
    defensive_rebounds_per_game: Optional[float] = None
    total_rebounds_per_game: Optional[float] = None
    assists_per_game: Optional[float] = None
    steals_per_game: Optional[float] = None
    turnovers_per_game: Optional[float] = None
    blocks_favour_per_game: Optional[float] = None
    blocks_against_per_game: Optional[float] = None
    fouls_committed_per_game: Optional[float] = None
    fouls_received_per_game: Optional[float] = None
    valuation_per_game: Optional[float] = None

class Lig_TeamsDAO():
    @staticmethod
    def create_lig_teams(db, team):
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            # Convert Lig_Teams object to dictionary if necessary
            if isinstance(team, Lig_Teams):
                team = team.__dict__

            # Dynamically construct query based on provided keys
            columns = ", ".join(team.keys())
            placeholders = ", ".join(["%s"] * len(team))
            query = f"INSERT INTO LIG_TEAMS ({columns}) VALUES ({placeholders})"

            # Execute query with provided values
            cursor.execute(query, list(team.values()))
            connection.commit()

            print(f"Successfully created LIG_TEAMS with provided data.")

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
            cursor = connection.cursor()
            
            # Extract fields from the `team` object
            fields_to_update = {}
            if team.season_team_id is not None:
                fields_to_update['season_team_id'] = team.season_team_id
            if team.games_played is not None:    
                fields_to_update['games_played'] = team.games_played
            if team.minutes_played is not None:
                fields_to_update['minutes_played'] = team.minutes_played
            if team.points is not None:
                fields_to_update['points'] = team.points
            if team.two_points_made is not None:
                fields_to_update['two_points_made'] = team.two_points_made
            if team.two_points_attempted is not None:
                fields_to_update['two_points_attempted'] = team.two_points_attempted
            if team.three_points_made is not None:
                fields_to_update['three_points_made'] = team.three_points_made
            if team.three_points_attempted is not None:
                fields_to_update['three_points_attempted'] = team.three_points_attempted
            if team.free_throws_made is not None:
                fields_to_update['free_throws_made'] = team.free_throws_made
            if team.free_throws_attempted is not None:
                fields_to_update['free_throws_attempted'] = team.free_throws_attempted
            if team.offensive_rebounds is not None:
                fields_to_update['offensive_rebounds'] = team.offensive_rebounds
            if team.defensive_rebounds is not None:
                fields_to_update['defensive_rebounds'] = team.defensive_rebounds
            if team.total_rebounds is not None:
                fields_to_update['total_rebounds'] = team.total_rebounds
            if team.assists is not None:
                fields_to_update['assists'] = team.assists
            if team.steals is not None:
                fields_to_update['steals'] = team.steals
            if team.turnovers is not None:
                fields_to_update['turnovers'] = team.turnovers
            if team.blocks_favour is not None:
                fields_to_update['blocks_favour'] = team.blocks_favour
            if team.blocks_against is not None:
                fields_to_update['blocks_against'] = team.blocks_against
            if team.fouls_committed is not None:
                fields_to_update['fouls_committed'] = team.fouls_committed
            if team.fouls_received is not None:
                fields_to_update['fouls_received'] = team.fouls_received
            if team.valuation is not None:
                fields_to_update['valuation'] = team.valuation
            if team.minutes_per_game is not None:
                fields_to_update['minutes_per_game'] = team.minutes_per_game
            if team.points_per_game is not None:
                fields_to_update['points_per_game'] = team.points_per_game
            if team.two_points_made_per_game is not None:
                fields_to_update['two_points_made_per_game'] = team.two_points_made_per_game
            if team.two_points_attempted_per_game is not None:
                fields_to_update['two_points_attempted_per_game'] = team.two_points_attempted_per_game
            if team.two_points_percentage is not None:
                fields_to_update['two_points_percentage'] = team.two_points_percentage
            if team.three_points_made_per_game is not None:
                fields_to_update['three_points_made_per_game'] = team.three_points_made_per_game
            if team.three_points_attempted_per_game is not None:
                fields_to_update['three_points_attempted_per_game'] = team.three_points_attempted_per_game
            if team.three_points_percentage is not None:
                fields_to_update['three_points_percentage'] = team.three_points_percentage
            if team.free_throws_made_per_game is not None:
                fields_to_update['free_throws_made_per_game'] = team.free_throws_made_per_game
            if team.free_throws_attempted_per_game is not None:
                fields_to_update['free_throws_attempted_per_game'] = team.free_throws_attempted_per_game
            if team.free_throws_percentage is not None:
                fields_to_update['free_throws_percentage'] = team.free_throws_percentage
            if team.offensive_rebounds_per_game is not None:
                fields_to_update['offensive_rebounds_per_game'] = team.offensive_rebounds_per_game
            if team.defensive_rebounds_per_game is not None:
                fields_to_update['defensive_rebounds_per_game'] = team.defensive_rebounds_per_game
            if team.total_rebounds_per_game is not None:
                fields_to_update['total_rebounds_per_game'] = team.total_rebounds_per_game
            if team.assists_per_game is not None:
                fields_to_update['assists_per_game'] = team.assists_per_game
            if team.steals_per_game is not None:
                fields_to_update['steals_per_game'] = team.steals_per_game
            if team.turnovers_per_game is not None:
                fields_to_update['turnovers_per_game'] = team.turnovers_per_game
            if team.blocks_favour_per_game is not None:
                fields_to_update['blocks_favour_per_game'] = team.blocks_favour_per_game
            if team.blocks_against_per_game is not None:
                fields_to_update['blocks_against_per_game'] = team.blocks_against_per_game
            if team.fouls_committed_per_game is not None:
                fields_to_update['fouls_committed_per_game'] = team.fouls_committed_per_game
            if team.fouls_received_per_game is not None:
                fields_to_update['fouls_received_per_game'] = team.fouls_received_per_game
            if team.valuation_per_game is not None:
                fields_to_update['valuation_per_game'] = team.valuation_per_game
            

 
            # Construct dynamic SQL query
            if not fields_to_update:
                raise ValueError("No fields to update were provided.")
            
            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"""
            UPDATE LIG_TEAMS
            SET {set_clause}
            WHERE season_team_id = %s
            """
            
            # Prepare values for the query
            values = list(fields_to_update.values())
            values.append(team.season_team_id)  # Add identifier for WHERE clause

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


    @staticmethod
    def get_paginated_lig_teams(db: db, offset: int = 0, limit: int = 25, columns: list = None) -> list:
        """
        Fetch paginated data from the LIG_TEAMS table with specified columns.
        
        Args:
            db: Database connection.
            offset: Starting row index.
            limit: Number of rows to fetch.
            columns: List of columns to select (default: all columns).

        Returns:
            A list of Lig_Teams objects.
        """
        try:
            connection = db.get_connection()
            
            # Build the SELECT query with the specified columns
            selected_columns = ", ".join(columns) if columns else "*"
            query = f"""
                SELECT {selected_columns} FROM LIG_TEAMS
                LIMIT %s OFFSET %s
            """
            
            cursor = connection.cursor()
            cursor.execute(query, (limit, offset))
            teams = cursor.fetchall()

            if teams is None:
                return None

            # Map fetched rows to Lig_Teams objects
            if columns:  # Use only the specified columns
                return [dict(zip(columns, team)) for team in teams]
            else:  # Use all columns
                return [Lig_Teams(*team) for team in teams]
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_total_lig_teams(db: db) -> int:
        """
        Fetch total number of rows in the LIG_TEAMS table.
        """
        try:
            connection = db.get_connection()
            query = "SELECT COUNT(*) FROM LIG_TEAMS"
            cursor = connection.cursor()
            cursor.execute(query)
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
