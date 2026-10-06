import sqlite3
from collections.abc import Generator

DATABASE_URL = "links.db"

def get_db() -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(DATABASE_URL)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
    finally:
        connection.close()


def init_db() -> None:
    connection = sqlite3.connect(DATABASE_URL)
    connection.execute("""
    CREATE TABLE IF NOT EXISTS links (
    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    original_url TEXT NOT NULL UNIQUE,
    clicks INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    last_clicked_at TEXT
    
    )
    """)
    connection.commit()
    connection.close()