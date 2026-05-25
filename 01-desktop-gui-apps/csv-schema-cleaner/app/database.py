import sqlite3


class ConfigStore:
    """
    Simple SQLite-based configuration storage.
    Used to save and retrieve profile mappings (e.g., column mappings)
    in a lightweight local database.
    """

    def __init__(self):
        """
        Initialize database connection and ensure required table exists.
        """
        # Connect to local SQLite database file
        self.conn = sqlite3.connect("settings.db")

        # Create a cursor object to execute SQL queries
        self.cursor = self.conn.cursor()

        # Create table if it does not already exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles 
            (
                id INTEGER PRIMARY KEY,
                name TEXT,
                column_map TEXT
            )
        """)

        # Commit schema changes to database
        self.conn.commit()

    def save_profile(self, name, mapping):
        """
        Save a configuration profile into the database.

        Args:
            name (str): Name of the profile
            mapping (dict or str): Column mapping configuration
        """
        # Insert profile data into the table
        self.cursor.execute(
            "INSERT INTO profiles (name, column_map) VALUES (?, ?)",
            (name, str(mapping))
        )

        # Commit transaction to persist changes
        self.conn.commit()