from dataclasses import dataclass
from datetime import datetime
from db.db import db
import mysql.connector
# season_player_id VARCHAR(50) PRIMARY KEY,
#     season_team_id VARCHAR(50),
#     player VARCHAR(100),
#     games_played INT,
#     games_started INT,
#     minutes_played FLOAT,
#     points INT,

@dataclass
class Player:
    season_player_id: str
    season_team_id: str
    player: str
    games_played: int
    games_started: int
    minutes_played: float
    points: int

class PlayersDAO():
    @staticmethod
    def create_player(db: db, player: Player) -> None:
        try:
            connection  = db.get_connection()
            cursor = db.connection.cursor()
            query = """
                INSERT INTO CUP_PLAYERS (
                season_player_id,
                season_team_id,
                player,
                games_played,
                games_started,
                minutes_played,
                points
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                player.season_player_id,
                player.season_team_id,
                player.player,
                player.games_played,
                player.games_started,
                player.minutes_played,
                player.points
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_player(db: db, player_id: str) -> Player:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM CUP_PLAYERS WHERE player_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (player_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return Player(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_all_players(db: db) -> list:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM CUP_PLAYERS
            """
            cursor = connection.cursor()
            cursor.execute(query)
            players = cursor.fetchall()
            if players is None:
                return None
            #! special return might not be needed but we will see
            return [Player(*player) for player in players]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()  
    
    
    @staticmethod
    def update_player(db: db, player:Player) -> None:
        try:
            connection = db.get_connection()
            query = """
                UPDATE CUP_PLAYERS SET
                    season_team_id = %s,
                    player = %s,
                    games_played = %s,
                    games_started = %s,
                    minutes_played = %s,
                    points = %s
                WHERE season_player_id = %s
            """

            cursor = connection.cursor()
            cursor.execute(query, (
                player.season_team_id,
                player.player,
                player.games_played,
                player.games_started,
                player.minutes_played,
                player.points,
                player.season_player_id
            ))
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
                DELETE FROM CUP_PLAYERS WHERE season_player_id = %s
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
            




