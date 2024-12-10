from dataclasses import dataclass
from datetime import datetime
from app.db.db import db
import mysql.connector
from typing import Optional

@dataclass
class Team:
    abbreviation: Optional[str] = None
    full_name: Optional[str] = None
    logo_url: Optional[str] = None

class TeamsDAO():
    @staticmethod
    def get_team(db: db, abbreviation: Optional[str] = None, full_name: Optional[str] = None) -> Optional[Team]:
        if not abbreviation and not full_name:
            raise ValueError("Either abbreviation or full_name must be provided.")

        try:
            connection = db.get_connection()
            query = "SELECT abbreviation, full_name, logo_url FROM teams WHERE"
            params = []

            # Build the query based on provided parameters
            if abbreviation:
                query += " abbreviation = %s"
                params.append(abbreviation)
            elif full_name:
                query += " full_name = %s"
                params.append(full_name)

            query += " LIMIT 1;"  # Ensure only one result is returned

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, tuple(params))
            result = cursor.fetchone()

            if result:
                return Team(
                    abbreviation=result.get("abbreviation"),
                    full_name=result.get("full_name"),
                    logo_url=result.get("logo_url")
                )
            return None  # No team found

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()
