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
    season_player_id: Optional[str]
    season_team_id: Optional[str]
    player: Optional[str]
    games_played: Optional[int]
    games_started: Optional[int]
    minutes_played: Optional[float]
    points: Optional[int]
    two_points_made: Optional[int]
    two_points_attempted: Optional[int]
    three_points_made: Optional[int]
    three_points_attempted: Optional[int]
    free_throws_made: Optional[int]
    free_throws_attempted: Optional[int]
    offensive_rebounds: Optional[int]
    defensive_rebounds: Optional[int]
    total_rebounds: Optional[int]
    assists: Optional[int]
    steals: Optional[int]
    turnovers: Optional[int]
    blocks_favour: Optional[int]
    blocks_against: Optional[int]
    fouls_committed: Optional[int]
    fouls_received: Optional[int]
    valuation: Optional[int]
    minutes_per_game: Optional[float]
    points_per_game: Optional[float]
    two_points_made_per_game: Optional[float]
    two_points_attempted_per_game: Optional[float]
    two_points_percentage: Optional[float]
    three_points_made_per_game: Optional[float]
    three_points_attempted_per_game: Optional[float]
    three_points_percentage: Optional[float]
    free_throws_made_per_game: Optional[float]
    free_throws_attempted_per_game: Optional[float]
    free_throws_percentage: Optional[float]
    offensive_rebounds_per_game: Optional[float]
    defensive_rebounds_per_game: Optional[float]
    total_rebounds_per_game: Optional[float]
    assists_per_game: Optional[float]
    steals_per_game: Optional[float]
    turnovers_per_game: Optional[float]
    blocks_favour_per_game: Optional[float]
    blocks_against_per_game: Optional[float]
    fouls_committed_per_game: Optional[float]
    fouls_received_per_game: Optional[float]
    valuation_per_game: Optional[float]

class Lig_PlayersDAO():
    @staticmethod
    def create_Lig_Players(db: db, player: Lig_Player) -> None:
        try:
            connection  = db.get_connection()
            cursor = db.connection.cursor()
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
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()
    
    @staticmethod
    def get_Lig_Player(db: db, season_player_id: str) -> Lig_Player: 
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM LIG_PLAYERS WHERE player_id = %s
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
    def get_all_Lig_Players(db: db) -> list:
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
    def update_Lig_Player(db: db, player:Lig_Player) -> None:
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            # Extract fields from player object

            fields_to_update = {}
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
            cursor.execute(query, (player_id,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    @staticmethod
    def get_paginated_cup_teams(db: db, offset: int = 0, limit: int = 25, columns: list = None, filters: dict = None, sort_by: str = None, order: str = 'asc') -> list:
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

        




