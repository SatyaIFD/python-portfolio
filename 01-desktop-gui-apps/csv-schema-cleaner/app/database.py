import sqlite3
import json

class ConfigStore:
    """
    SQLite-based storage for validation profiles.
    Handles JSON serialization for complex column mappings.
    """

    def __init__(self, db_path="settings.db"):
        # Using check_same_thread=False allows PySide6 threads to access the DB
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._migrate()

    def _migrate(self):
        """Ensures the schema is up to date."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                column_map TEXT,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def save_profile(self, name, mapping):
        """
        Saves or updates a profile. 
        Converts dictionary mapping to a JSON string.
        """
        json_mapping = json.dumps(mapping)
        query = """
            INSERT INTO profiles (name, column_map)
            VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET column_map = excluded.column_map
        """
        try:
            self.cursor.execute(query, (name, json_mapping))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Database Error: {e}")
            return False

    def get_profile(self, name):
        """Retrieves a profile and converts JSON back to a dict."""
        self.cursor.execute("SELECT column_map FROM profiles WHERE name = ?", (name,))
        row = self.cursor.fetchone()
        if row:
            return json.loads(row[0])
        return None

    def list_profiles(self):
        """Returns a list of all saved profile names."""
        self.cursor.execute("SELECT name FROM profiles ORDER BY last_used DESC")
        return [row[0] for row in self.cursor.fetchall()]

    def delete_profile(self, name):
        """Removes a profile from the database."""
        self.cursor.execute("DELETE FROM profiles WHERE name = ?", (name,))
        self.conn.commit()

    def close(self):
        """Properly closes the connection."""
        self.conn.close()