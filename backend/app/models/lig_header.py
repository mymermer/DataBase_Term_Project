from dataclasses import dataclass
from datetime import datetime
from db.db import db
import mysql.connector

# game_id VARCHAR(50) PRIMARY KEY,
# game VARCHAR(50),
# date_of_game DATE,
# time_of_game TIME,
# round_of_game INT,
# phase VARCHAR(50),
# season_team_id_a VARCHAR(50),
# season_team_id_b VARCHAR(50),
# score_a INT,
# score_b INT,
# team_a VARCHAR(50),
# team_b VARCHAR(50),
# coach_a VARCHAR(50),
# coach_b VARCHAR(50),
# game_time TIME,
# referee_1 VARCHAR(50),
# referee_2 VARCHAR(50),
# referee_3 VARCHAR(50),
# stadium VARCHAR(50),
# capacity INT,
# fouls_a INT,
# fouls_b INT,
# timeouts_a INT,
# timeouts_b INT,
# score_quarter_1_a INT,
# score_quarter_2_a INT,
# score_quarter_3_a INT,
# score_quarter_4_a INT,
# score_quarter_1_b INT,
# score_quarter_2_b INT,
# score_quarter_3_b INT,
# score_quarter_4_b INT,
# score_extra_time_1_a INT,
# score_extra_time_2_a INT,
# score_extra_time_3_a INT,
# score_extra_time_4_a INT,
# score_extra_time_1_b INT,
# score_extra_time_2_b INT,
# score_extra_time_3_b INT,
# score_extra_time_4_b INT,
# winner CHAR(6)

@dataclass
class Lig_Header:
    game_id: str
    game: str
    date_of_game: datetime
    time_of_game: datetime
    round_of_game: int
    phase: str
    season_team_id_a: str
    season_team_id_b: str
    score_a: int
    score_b: int
    team_a: str
    team_b: str
    coach_a: str
    coach_b: str
    game_time: datetime
    referee_1: str
    referee_2: str
    referee_3: str
    stadium: str
    capacity: int
    fouls_a: int
    fouls_b: int
    timeouts_a: int
    timeouts_b: int
    score_quarter_1_a: int
    score_quarter_2_a: int
    score_quarter_3_a: int
    score_quarter_4_a: int
    score_quarter_1_b: int
    score_quarter_2_b: int
    score_quarter_3_b: int
    score_quarter_4_b: int
    score_extra_time_1_a: int
    score_extra_time_2_a: int
    score_extra_time_3_a: int
    score_extra_time_4_a: int
    score_extra_time_1_b: int
    score_extra_time_2_b: int
    score_extra_time_3_b: int
    score_extra_time_4_b: int
    winner: str

class Lig_HeaderDAO():
    @staticmethod
    def create_lig_header(db: db, header: Lig_Header) -> None:
        try:
            connection  = db.get_connection()
            cursor = db.connection.cursor()
            query = """
                INSERT INTO LIG_HEADER (
                game_id,
                game,
                date_of_game,
                time_of_game,
                round_of_game,
                phase,
                season_team_id_a,
                season_team_id_b,
                score_a,
                score_b,
                team_a,
                team_b,
                coach_a,
                coach_b,
                game_time,
                referee_1,
                referee_2,
                referee_3,
                stadium,
                capacity,
                fouls_a,
                fouls_b,
                timeouts_a,
                timeouts_b,
                score_quarter_1_a,
                score_quarter_2_a,
                score_quarter_3_a,
                score_quarter_4_a,
                score_quarter_1_b,
                score_quarter_2_b,
                score_quarter_3_b,
                score_quarter_4_b,
                score_extra_time_1_a,
                score_extra_time_2_a,
                score_extra_time_3_a,
                score_extra_time_4_a,
                score_extra_time_1_b,
                score_extra_time_2_b,
                score_extra_time_3_b,
                score_extra_time_4_b,
                winner
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """

            cursor.execute(query, (
                header.game_id,
                header.game,
                header.date_of_game,
                header.time_of_game,
                header.round_of_game,
                header.phase,
                header.season_team_id_a,
                header.season_team_id_b,
                header.score_a,
                header.score_b,
                header.team_a,
                header.team_b,
                header.coach_a,
                header.coach_b,
                header.game_time,
                header.referee_1,
                header.referee_2,
                header.referee_3,
                header.stadium,
                header.capacity,
                header.fouls_a,
                header.fouls_b,
                header.timeouts_a,
                header.timeouts_b,
                header.score_quarter_1_a,
                header.score_quarter_2_a,
                header.score_quarter_3_a,
                header.score_quarter_4_a,
                header.score_quarter_1_b,
                header.score_quarter_2_b,
                header.score_quarter_3_b,
                header.score_quarter_4_b,
                header.score_extra_time_1_a,
                header.score_extra_time_2_a,
                header.score_extra_time_3_a,
                header.score_extra_time_4_a,
                header.score_extra_time_1_b,
                header.score_extra_time_2_b,
                header.score_extra_time_3_b,
                header.score_extra_time_4_b,
                header.winner
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_lig_header(db: db, game_id: str) -> Lig_Header:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM LIG_HEADER WHERE game_id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (game_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return Lig_Header(*result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_all_lig_headers(db: db) -> list:
        try:
            connection = db.get_connection()
            query = """
                SELECT * FROM LIG_HEADER
            """
            cursor = connection.cursor()
            cursor.execute(query)
            headers = cursor.fetchall()
            if headers is None:
                return None
            #! special return might not be needed but we will see
            return [Lig_Header(*header) for header in headers]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()  
    
    
    @staticmethod
    def update_lig_header(db: db, header: Lig_Header) -> None:
        try:
            connection = db.get_connection()
            query = """
            UPDATE LIG_HEADER SET
            game = %s,
            date_of_game = %s,
            time_of_game = %s,
            round_of_game = %s,
            phase = %s,
            season_team_id_a = %s,
            season_team_id_b = %s,
            score_a = %s,
            score_b = %s,
            team_a = %s,
            team_b = %s,
            coach_a = %s,
            coach_b = %s,
            game_time = %s,
            referee_1 = %s,
            referee_2 = %s,
            referee_3 = %s,
            stadium = %s,
            capacity = %s,
            fouls_a = %s,
            fouls_b = %s,
            timeouts_a = %s,
            timeouts_b = %s,
            score_quarter_1_a = %s,
            score_quarter_2_a = %s,
            score_quarter_3_a = %s,
            score_quarter_4_a = %s,
            score_quarter_1_b = %s,
            score_quarter_2_b = %s,
            score_quarter_3_b = %s,
            score_quarter_4_b = %s,
            score_extra_time_1_a = %s,
            score_extra_time_2_a = %s,
            score_extra_time_3_a = %s,
            score_extra_time_4_a = %s,
            score_extra_time_1_b = %s,
            score_extra_time_2_b = %s,
            score_extra_time_3_b = %s,
            score_extra_time_4_b = %s,
            winner = %s
            WHERE game_id = %s
            """

            cursor = connection.cursor()
            cursor.execute(query, (
            header.game,
            header.date_of_game,
            header.time_of_game,
            header.round_of_game,
            header.phase,
            header.season_team_id_a,
            header.season_team_id_b,
            header.score_a,
            header.score_b,
            header.team_a,
            header.team_b,
            header.coach_a,
            header.coach_b,
            header.game_time,
            header.referee_1,
            header.referee_2,
            header.referee_3,
            header.stadium,
            header.capacity,
            header.fouls_a,
            header.fouls_b,
            header.timeouts_a,
            header.timeouts_b,
            header.score_quarter_1_a,
            header.score_quarter_2_a,
            header.score_quarter_3_a,
            header.score_quarter_4_a,
            header.score_quarter_1_b,
            header.score_quarter_2_b,
            header.score_quarter_3_b,
            header.score_quarter_4_b,
            header.score_extra_time_1_a,
            header.score_extra_time_2_a,
            header.score_extra_time_3_a,
            header.score_extra_time_4_a,
            header.score_extra_time_1_b,
            header.score_extra_time_2_b,
            header.score_extra_time_3_b,
            header.score_extra_time_4_b,
            header.winner,
            header.game_id  # The identifier in the WHERE clause
            ))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_lig_header(db: db, game_id: str) -> None:
        try:
            connection = db.get_connection()
            query = """
                DELETE FROM LIG_HEADER WHERE game_id = %s
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