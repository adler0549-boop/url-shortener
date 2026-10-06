import secrets
import sqlite3
import string
from datetime import datetime, timezone
from repository import create_link, get_link_by_url, get_link_by_code, register_click


def generate_code(length: int=6) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(length))


def create_short_link(db: sqlite3.Connection, original_url: str) -> tuple[str, bool]:
    existing = get_link_by_url(db, original_url)

    if existing:
        return existing["code"], False

    while True:
        code = generate_code()

        try:
            create_link(db=db, code=code, url=original_url, created_at=datetime.now(timezone.utc),)
            return code, True
        except sqlite3.IntegrityError:
            continue


def get_link(db: sqlite3.Connection, code: str) -> sqlite3.Row | None:
    return get_link_by_code(db, code)


def click_link(db: sqlite3.Connection, code: str) -> sqlite3.Row | None:
    link = get_link_by_code(db, code)

    if link is None:
        return None

    register_click(db=db, code=code, clicked_at=datetime.now(timezone.utc),)
    return get_link_by_code(db, code)