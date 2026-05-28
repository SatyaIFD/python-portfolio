import sqlite3
from pathlib import Path
from app.utils.logger import get_logger

logger = get_logger(__name__)

class CatalogDatabase:
    """Manages the persistent SQLite indexing layer for all sorted metadata profiles."""
    
    def __init__(self, db_path: str = "file_catalog.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initializes tables for tracking file properties and historical operations."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS file_catalog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_name TEXT NOT NULL,
                    current_path TEXT NOT NULL UNIQUE,
                    file_extension TEXT,
                    file_size_bytes INTEGER,
                    detected_category TEXT,
                    processed_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        logger.info(f"Metadata catalog indexing database verified at: {self.db_path}")

    def catalog_file(self, original_name: str, current_path: Path, extension: str, size: int, category: str):
        """Inserts or updates a file's state registry metadata within the index."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO file_catalog 
                    (original_name, current_path, file_extension, file_size_bytes, detected_category)
                    VALUES (?, ?, ?, ?, ?)
                """, (original_name, str(current_path), extension, size, category))
                conn.commit()
            logger.info(f"Indexed entry for '{original_name}' under category '{category}'")
        except sqlite3.Error as e:
            logger.error(f"Failed to catalog file metadata for {original_name}: {str(e)}")