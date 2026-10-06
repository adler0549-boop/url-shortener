import sqlite3
from datetime import datetime
from schemas import LinkStats

def get_link_by_url(db: sqlite3.Connection, url: str) -> sqlite3.Row | None:
    cursor = db.execute(""" SELECT * FROM links WHERE original_url = ?""", (url,),)
    return cursor.fetchone()


def get_link_by_code(db: sqlite3.Connection, code: str) -> sqlite3.Row | None:
    cursor = db.execute(""" SELECT * FROM links WHERE code = ?""", (code,),)
    return cursor.fetchone()


def create_link(db: sqlite3.Connection, code: str, url: str, created_at: datetime) -> None:
    db.execute(""" INSERT INTO links (code, original_url, created_at)
                        VALUES (?, ?, ?)""",(code, url, created_at.isoformat()), )
    db.commit()


def register_click(db: sqlite3.Connection, code: str, clicked_at: datetime) -> None:
    db.execute(""" UPDATE links
                    SET clicks = clicks + 1,
                        last_clicked_at = ?
                    WHERE code = ?
                    """,(clicked_at.isoformat(), code),)
    db.commit()


def get_stats(db: sqlite3.Connection, link: sqlite3.Row) -> LinkStats:
    return LinkStats(code=link["code"],
                     original_url=link["original_url"],
                     clicks=link["clicks"],
                     created_at=datetime.fromisoformat(link["created_at"]),
                     last_clicked_at=(datetime.fromisoformat(link["last_clicked_at"])
                     if link["last_clicked_at"]
                     else None
                     ),
                     )


