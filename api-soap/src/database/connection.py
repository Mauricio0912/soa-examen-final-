import sqlite3
from typing import Optional

from src.config import get_settings


class DatabaseConnection:
    def __init__(self, db_path: str = ':memory:'):
        self._db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        if self._connection is None:
            self._connection = sqlite3.connect(
                self._db_path,
                check_same_thread=False
            )
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def close(self) -> None:
        if self._connection:
            self._connection.close()
            self._connection = None

    def init_schema(self) -> None:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL
            )
        ''')
        conn.commit()

    @property
    def connection(self) -> sqlite3.Connection:
        return self.connect()


_database: Optional[DatabaseConnection] = None


def get_database() -> DatabaseConnection:
    global _database
    if _database is None:
        settings = get_settings()
        _database = DatabaseConnection(settings.db_path)
    return _database
