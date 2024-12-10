from dataclasses import dataclass
from datetime import datetime
from app.db.db import db
import mysql.connector
from typing import Optional

class Team:
    abbreviation: Optional[str] = None
    full_name: Optional[str] = None
    logo_url: Optional[str] = None

class TeamsDAO():
    @staticmethod
    def get_cup_points(db: db, abbreviation: Optional[str] = None, full_name: Optional[str] = None) -> Team:
        query = "SELECT abbreviation, full_name, logo_url FROM teams WHERE"
        params = []
        
        # If abbreviation is provided, add it to the WHERE clause
        if abbreviation:
            query += " abbreviation = %s"
            params.append(abbreviation)
        # If only full name is provided, use it to find the team
        elif full_name:
            query += " full_name = %s"
            params.append(full_name)
        else:
            raise ValueError("Either abbreviation or full_name must be provided.")
        
        query += " LIMIT 1;"  # Ensure we only get the first result in case of multiple rows with the same abbreviation
        
        # Execute the query
        try:
            connection = mysql.connector.connect(
                host=db.host,
                user=db.user,
                password=db.password,
                database=db.database
            )
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, tuple(params))
            result = cursor.fetchone()  # Get the first row

            if result:
                team = Team()
                team.abbreviation = result.get("abbreviation")
                team.full_name = result.get("full_name")
                team.logo_url = result.get("logo_url")
                return team
            else:
                return None  # No team found

        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
