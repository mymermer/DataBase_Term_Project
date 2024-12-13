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
    def get_teams(db, abbreviations: list = None, full_names: list = None) -> list:
        if not abbreviations and not full_names:
            raise ValueError("Either abbreviations or full_names must be provided.")

        if abbreviations and full_names and len(abbreviations) != len(full_names):
            raise ValueError("The number of abbreviations and full_names must match.")

        try:
            connection = db.get_connection()
            cursor = connection.cursor(dictionary=True)

            results = []
            if abbreviations and full_names:
                # Match both abbreviations and full_names in a pairwise manner
                for abbr, fname in zip(abbreviations, full_names):
                    query = """
                        SELECT abbreviation, full_name, logo_url
                        FROM teams
                        WHERE abbreviation = %s AND full_name = %s LIMIT 1;
                    """
                    cursor.execute(query, (abbr, fname))
                    result = cursor.fetchone()
                    if not result:
                        raise ValueError(f"No team found for abbreviation '{abbr}' and full_name '{fname}'.")
                    results.append(result)
            elif abbreviations:
                # Query for each abbreviation
                query = """
                    SELECT abbreviation, full_name, logo_url
                    FROM teams
                    WHERE abbreviation IN (%s);
                """ % ','.join(['%s'] * len(abbreviations))
                cursor.execute(query, tuple(abbreviations))
                results = cursor.fetchall()
            elif full_names:
                # Query for each full_name
                query = """
                    SELECT abbreviation, full_name, logo_url
                    FROM teams
                    WHERE full_name IN (%s);
                """ % ','.join(['%s'] * len(full_names))
                cursor.execute(query, tuple(full_names))
                results = cursor.fetchall()

            # Convert results to Team objects
            return [Team(
                abbreviation=row["abbreviation"],
                full_name=row["full_name"],
                logo_url=row["logo_url"]
            ) for row in results]

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            return []
        finally:
            cursor.close()
            connection.close()
