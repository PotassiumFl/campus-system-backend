from typing import Optional

from db.connection import get_connection


def user_exists(name: str) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM user WHERE UNAME=%s LIMIT 1", (name,))
            return cur.fetchone() is not None
    finally:
        conn.close()


def insert_user(name: str, password: int) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO user (UNAME, PASSWORD) VALUES (%s, %s)",
                (name, password),
            )
        conn.commit()
        return True
    finally:
        conn.close()


def get_password(name: str) -> Optional[int]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT PASSWORD FROM user WHERE UNAME=%s LIMIT 1",
                (name,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            return int(row[0])
    finally:
        conn.close()

