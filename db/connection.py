import os
from pathlib import Path
from threading import Lock
from typing import Any, Literal, Sequence

from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)


def _db_config():
    return {
        "host": os.environ["DB_HOST"],
        "port": int(os.environ["DB_PORT"]),
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "database": os.environ["DB_NAME"],
    }


_pool: pooling.MySQLConnectionPool | None = None
_pool_lock = Lock()


def _get_pool() -> pooling.MySQLConnectionPool:
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                raw = os.environ.get("DB_POOL_SIZE", "8")
                try:
                    size = max(1, int(raw))
                except ValueError:
                    size = 8
                _pool = pooling.MySQLConnectionPool(
                    pool_name="dbdesignpy_pool",
                    pool_size=size,
                    pool_reset_session=True,
                    **_db_config(),
                )
    return _pool


def _get_connection():
    return _get_pool().get_connection()


def run(
    sql: str,
    params: Sequence[Any] | None = None,
    commit: bool = False,
    fetch: Literal["none", "one", "all"] = "none",
) -> Any:
    """Execute ``sql`` using a pooled connection; commit when ``commit``.

    Rows use the same shape as JSON (``dict`` mapping column name -> value):

    - ``fetch`` ``none``: ``None``
    - ``fetch`` ``one``: ``dict`` or ``None``
    - ``fetch`` ``all``: ``list`` of ``dict`` (may be empty)

    Values may still be Python types (e.g. ``Decimal``, ``datetime``) until you
    serialize for HTTP with :func:`json.dumps` or FastAPI's encoder.
    """
    conn = _get_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, params if params is not None else None)
            if fetch == "none":
                out: Any = None
            elif fetch == "one":
                out = cur.fetchone()
            else:
                out = cur.fetchall()
        if commit:
            conn.commit()
        return out
    finally:
        conn.close()


def insert_returning_last_id(
    sql: str,
    params: Sequence[Any] | None = None,
) -> int:
    """Execute INSERT on one connection and return ``LAST_INSERT_ID()`` (autoincrement).

    Pooling opens a fresh connection per :func:`run`; this keeps INSERT and
    ``lastrowid`` on the same session.
    """
    conn = _get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params if params is not None else None)
            new_id = cur.lastrowid
        conn.commit()
        if new_id is None:
            raise RuntimeError("INSERT did not produce lastrowid (not an AUTO_INCREMENT insert?)")
        return int(new_id)
    finally:
        conn.close()
