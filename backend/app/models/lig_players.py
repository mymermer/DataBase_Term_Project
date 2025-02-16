from dataclasses import dataclass
from datetime import datetime
from app.db.db import db
import mysql.connector
from typing import Optional


#    season_player_id VARCHAR(50) PRIMARY KEY,
#    season_team_id VARCHAR(50),
#    player VARCHAR(100),
#    games_played INT,
#    games_started INT,
#    minutes_played FLOAT,
#    points INT,
#    two_points_made INT,
#    two_points_attempted INT,
#    three_points_made INT,
#    three_points_attempted INT,
#    free_throws_made INT,
#    free_throws_attempted INT,
#    offensive_rebounds INT,
#    defensive_rebounds INT,
#    total_rebounds INT,
#    assists INT,
#    steals INT,
#    turnovers INT,
#    blocks_favour INT,
#    blocks_against INT,
#    fouls_committed INT,
#    fouls_received INT,
#    valuation INT,
#    minutes_per_game FLOAT,
#    points_per_game FLOAT,
#    two_points_made_per_game FLOAT,
#    two_points_attempted_per_game FLOAT,
#    two_points_percentage FLOAT,
#    three_points_made_per_game FLOAT,
#    three_points_attempted_per_game FLOAT,
#    three_points_percentage FLOAT,
#    free_throws_made_per_game FLOAT,
#    free_throws_attempted_per_game FLOAT,
#    free_throws_percentage FLOAT,
#    offensive_rebounds_per_game FLOAT,
#    defensive_rebounds_per_game FLOAT,
#    total_rebounds_per_game FLOAT,
#    assists_per_game FLOAT,
#    steals_per_game FLOAT,
#    turnovers_per_game FLOAT,
#    blocks_favour_per_game FLOAT,
#    blocks_against_per_game FLOAT,
#    fouls_committed_per_game FLOAT,
#    fouls_received_per_game FLOAT,
#    valuation_per_game FLOAT

@dataclass
class Lig_Player:
    season_player_id: Optional[str] #? why can the primary key be optional?
    season_team_id: Optional[str] = None
    player: Optional[str] = None
    games_played: Optional[int] = None
    games_started: Optional[int] = None
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

class Lig_PlayersDAO():
    @staticmethod
    def create_lig_players(db: db, player: Lig_Player) -> None:
        try:
            connection  = db.get_connection()
            cursor = connection.cursor()
            if isinstance(player, Lig_Player):
                player = player.__dict__

            # Dynamically build the query string
            columns = ", ".join(player.keys())
            placeholders = ", ".join(["%s"] * len(player))
            query = f"INSERT INTO LIG_PLAYERS ({columns}) VALUES ({placeholders})"

            # Execute the query
            cursor.execute(query, list(player.values()))
            connection.commit()

        except mysql.connector.Error as err:
            print(f"DB Error: {err}")
            connection.rollback()
            raise
        except Exception as e:
            print(f"General Error: {e}")
            raise
        finally:
            # ? why close is conditional unlike the other methods
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()
    
    @staticmethod
    def get_lig_player(db: db, season_player_id: str) -> Lig_Player: 
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM LIG_PLAYERS WHERE season_player_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (season_player_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return Lig_Player(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_all_lig_players(db: db) -> list:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM Lig_PlayerS
            """
            cursor = connection.cursor()
            cursor.execute(query)
            players = cursor.fetchall()
            if players is None:
                return None
            return [Lig_Player(*player) for player in players]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()  
    
    
    @staticmethod
    def update_lig_player(db: db, player:Lig_Player) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            # Extract fields from player object

            fields_to_update = {}
            if player.season_player_id is not None:
                fields_to_update['season_player_id'] = player.season_player_id
            if player.season_team_id is not None:
                fields_to_update['season_team_id'] = player.season_team_id
            if player.player is not None:
                fields_to_update['player'] = player.player
            if player.games_played is not None:
                fields_to_update['games_played'] = player.games_played
            if player.games_started is not None:
                fields_to_update['games_started'] = player.games_started
            if player.minutes_played is not None:
                fields_to_update['minutes_played'] = player.minutes_played
            if player.points is not None:
                fields_to_update['points'] = player.points
            if player.two_points_made is not None:
                fields_to_update['two_points_made'] = player.two_points_made
            if player.two_points_attempted is not None:
                fields_to_update['two_points_attempted'] = player.two_points_attempted
            if player.three_points_made is not None:
                fields_to_update['three_points_made'] = player.three_points_made
            if player.three_points_attempted is not None:
                fields_to_update['three_points_attempted'] = player.three_points_attempted
            if player.free_throws_made is not None:
                fields_to_update['free_throws_made'] = player.free_throws_made
            if player.free_throws_attempted is not None:
                fields_to_update['free_throws_attempted'] = player.free_throws_attempted
            if player.offensive_rebounds is not None:
                fields_to_update['offensive_rebounds'] = player.offensive_rebounds
            if player.defensive_rebounds is not None:
                fields_to_update['defensive_rebounds'] = player.defensive_rebounds
            if player.total_rebounds is not None:
                fields_to_update['total_rebounds'] = player.total_rebounds
            if player.assists is not None:
                fields_to_update['assists'] = player.assists
            if player.steals is not None:
                fields_to_update['steals'] = player.steals
            if player.turnovers is not None:
                fields_to_update['turnovers'] = player.turnovers
            if player.blocks_favour is not None:
                fields_to_update['blocks_favour'] = player.blocks_favour
            if player.blocks_against is not None:
                fields_to_update['blocks_against'] = player.blocks_against
            if player.fouls_committed is not None:
                fields_to_update['fouls_committed'] = player.fouls_committed
            if player.fouls_received is not None:
                fields_to_update['fouls_received'] = player.fouls_received
            if player.valuation is not None:
                fields_to_update['valuation'] = player.valuation
            if player.minutes_per_game is not None:
                fields_to_update['minutes_per_game'] = player.minutes_per_game
            if player.points_per_game is not None:
                fields_to_update['points_per_game'] = player.points_per_game
            if player.two_points_made_per_game is not None:
                fields_to_update['two_points_made_per_game'] = player.two_points_made_per_game
            if player.two_points_attempted_per_game is not None:
                fields_to_update['two_points_attempted_per_game'] = player.two_points_attempted_per_game
            if player.two_points_percentage is not None:
                fields_to_update['two_points_percentage'] = player.two_points_percentage
            if player.three_points_made_per_game is not None:
                fields_to_update['three_points_made_per_game'] = player.three_points_made_per_game
            if player.three_points_attempted_per_game is not None:
                fields_to_update['three_points_attempted_per_game'] = player.three_points_attempted_per_game
            if player.three_points_percentage is not None:
                fields_to_update['three_points_percentage'] = player.three_points_percentage
            if player.free_throws_made_per_game is not None:
                fields_to_update['free_throws_made_per_game'] = player.free_throws_made_per_game
            if player.free_throws_attempted_per_game is not None:
                fields_to_update['free_throws_attempted_per_game'] = player.free_throws_attempted_per_game
            if player.free_throws_percentage is not None:
                fields_to_update['free_throws_percentage'] = player.free_throws_percentage
            if player.offensive_rebounds_per_game is not None:
                fields_to_update['offensive_rebounds_per_game'] = player.offensive_rebounds_per_game
            if player.defensive_rebounds_per_game is not None:
                fields_to_update['defensive_rebounds_per_game'] = player.defensive_rebounds_per_game
            if player.total_rebounds_per_game is not None:
                fields_to_update['total_rebounds_per_game'] = player.total_rebounds_per_game
            if player.assists_per_game is not None:
                fields_to_update['assists_per_game'] = player.assists_per_game
            if player.steals_per_game is not None:
                fields_to_update['steals_per_game'] = player.steals_per_game
            if player.turnovers_per_game is not None:
                fields_to_update['turnovers_per_game'] = player.turnovers_per_game
            if player.blocks_favour_per_game is not None:
                fields_to_update['blocks_favour_per_game'] = player.blocks_favour_per_game
            if player.blocks_against_per_game is not None:
                fields_to_update['blocks_against_per_game'] = player.blocks_against_per_game
            if player.fouls_committed_per_game is not None:
                fields_to_update['fouls_committed_per_game'] = player.fouls_committed_per_game
            if player.fouls_received_per_game is not None:
                fields_to_update['fouls_received_per_game'] = player.fouls_received_per_game
            if player.valuation_per_game is not None:
                fields_to_update['valuation_per_game'] = player.valuation_per_game
            
            
            # construct dynamic query
            if not fields_to_update:
                raise ValueError("No fields to update")
            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"""
            UPDATE Lig_PlayerS
            SET {set_clause}
            WHERE season_player_id = %s
            """
            values = list(fields_to_update.values())
            values.append(player.season_player_id)

            cursor.execute(query, tuple(values))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_player(db: db, player_id: str) -> None:
        try:
            connection = db.get_connection()
            query = """
                DELETE FROM LIG_PLAYERS WHERE season_player_id = %s
            """
            cursor = connection.cursor()
            # comma is needed to make it a tuple
            cursor.execute(query, (player_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
            
    @staticmethod
    def get_paginated_lig_player(db: db, offset: int = 0, limit: int = 25, columns: list = None, filters: dict = None, sort_by: str = None, order: str = 'asc') -> list:
        try:
            connection = db.get_connection()

            # build select
            selected_columns = ", ".join(columns) if columns else "*"

            # build where clause
            where_clauses = []
            params = []
            if filters:
                for column, value in filters.items():
                    where_clauses.append(f"{column} = %s")
                    params.append(value)

            where_clause = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

            # Add ORDER BY
            order_clause = ""
            if sort_by:
                if order.lower() not in ['asc', 'desc']:
                    order = 'asc'
                order_clause = f"ORDER BY {sort_by} {order.upper()}"

            query = f"""
                SELECT {selected_columns}
                FROM LIG_PLAYERS
                {where_clause}
                {order_clause}
                LIMIT %s OFFSET %s
            """

            params.extend([limit, offset])
            cursor = connection.cursor()
            cursor.execute(query, params)
            players = cursor.fetchall()

            if players is None:
                return None
            
            if columns:
                return [dict(zip(columns, player)) for player in players]
            else:
                return [Lig_Player(*player) for player in players]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_total_lig_players(db: db, filters: dict = None) -> int:
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
                SELECT COUNT(*) FROM LIG_PLAYERS
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

    # special to players

#    @staticmethod
    @staticmethod
    def get_distinct_teams_by_year(
        db: db,
        year: str
    ) -> list:
        """
        Fetch distinct team identifiers (e.g., 'PAM') from the LIG_PLAYERS table
        where the season_team_id starts with the given year.

        Args:
            db: Database connection object.
            year: The year to filter season_team_id, prefixed with 'E' (e.g., 'E2007').

        Returns:
            A list of distinct team identifiers (e.g., ['PAM', 'XYZ']).
        """
        try:
            connection = db.get_connection()

            # LIKE pattern to match the year at the start of season_team_id
            like_pattern = f"{year}_%"

            # Query to select distinct teams
            query = """
                SELECT DISTINCT 
                    SUBSTRING_INDEX(season_team_id, '_', -1) AS team_identifier
                FROM LIG_PLAYERS
                WHERE season_team_id LIKE %s
            """

            cursor = connection.cursor()
            cursor.execute(query, (like_pattern,))
            distinct_teams = cursor.fetchall()

            # Return the distinct teams as a flat list
            return [row[0] for row in distinct_teams]
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
    def get_players_point_percentage_by_season(db, season: str) :
        try:
            connection = db.get_connection()
            # ? why is this a dictionary
            cursor = connection.cursor(dictionary=True)

            query = f"""
            SELECT LIG_PLAYERS.points as player_points
            , LIG_PLAYERS.player as player_name
            , SUBSTRING_INDEX(LIG_TEAMS.season_team_id, '_', -1) AS team_name
            , LIG_TEAMS.points as team_points
            , LIG_PLAYERS.points/LIG_TEAMS.points as point_percentage
            FROM LIG_PLAYERS
            JOIN LIG_TEAMS
            ON LIG_PLAYERS.season_team_id = LIG_TEAMS.season_team_id
            WHERE LIG_PLAYERS.season_team_id LIKE %s
            """

            cursor.execute(query, (season + '%',))
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    @staticmethod
    def get_players_point_percentage_by_team_and_season(db, season: str, team: str):
        """
        Fetch player point percentages for a specific team in a selected season.

        Args:
            db: Database connection object.
            season: The season to filter by (e.g., '2023').
            team: The specific team to filter by (e.g., 'PAM').

        Returns:
            A list of dictionaries containing player points, player name, team name,
            team points, and the player's point percentage of the team.
        """
        try:
            connection = db.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = f"""
            SELECT 
                LIG_PLAYERS.points AS player_points,
                LIG_PLAYERS.player AS player_name,
                SUBSTRING_INDEX(LIG_TEAMS.season_team_id, '_', -1) AS team_name,
                LIG_TEAMS.points AS team_points,
                LIG_PLAYERS.points / LIG_TEAMS.points AS point_percentage
            FROM 
                LIG_PLAYERS
            JOIN 
                LIG_TEAMS
            ON 
                LIG_PLAYERS.season_team_id = LIG_TEAMS.season_team_id
            WHERE 
                LIG_PLAYERS.season_team_id LIKE %s
                AND SUBSTRING_INDEX(LIG_TEAMS.season_team_id, '_', -1) = %s
            """

            cursor.execute(query, (season + '%', team))
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()


