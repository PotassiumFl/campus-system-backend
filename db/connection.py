import mysql.connector

_DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "dbdesign",
}


def get_connection():
    """Create a new DB connection per call (safe for multi-requests)."""
    return mysql.connector.connect(**_DB_CONFIG)

