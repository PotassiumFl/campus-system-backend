"""Database access: use ``run`` from model layer; connection details stay here."""

from db.connection import insert_returning_last_id, run

__all__ = ["insert_returning_last_id", "run"]

