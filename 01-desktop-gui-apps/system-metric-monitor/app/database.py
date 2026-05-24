import sqlite3
import os
from datetime import datetime

DB_NAME = "pulse_telemetry.db"

def initialize_database():
    """Creates the metrics log table if it does not already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metric_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            metric_type TEXT NOT NULL,
            value REAL NOT NULL,
            alert_level TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_spike(metric_type, value, alert_level):
    """Inserts a resource anomaly or spike event into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO metric_logs (timestamp, metric_type, value, alert_level)
        VALUES (?, ?, ?, ?)
    """, (timestamp, metric_type, value, alert_level))
    
    conn.commit()
    conn.close()
    print(f"[{alert_level}] Logged {metric_type} spike: {value}% to local SQLite DB.")