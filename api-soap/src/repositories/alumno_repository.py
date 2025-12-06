from typing import Optional

from src.database import DatabaseConnection


class AlumnoRepository:
    def __init__(self, database: DatabaseConnection):
        self._db = database

    def _generate_matricula(self) -> str:
        cursor = self._db.connection.cursor()
        cursor.execute('SELECT MAX(id) FROM alumnos')
        result = cursor.fetchone()
        next_num = (result[0] or 0) + 1
        return f"k{next_num}"

    def create(self, nombre: str) -> dict:
        matricula = self._generate_matricula()
        cursor = self._db.connection.cursor()
        cursor.execute(
            'INSERT INTO alumnos (matricula, nombre) VALUES (?, ?)',
            (matricula, nombre)
        )
        self._db.connection.commit()

        return {
            'id': cursor.lastrowid,
            'matricula': matricula,
            'nombre': nombre
        }

    def find_by_id(self, id: int) -> Optional[dict]:
        cursor = self._db.connection.cursor()
        cursor.execute('SELECT * FROM alumnos WHERE id = ?', (id,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        return None

    def find_by_matricula(self, matricula: str) -> Optional[dict]:
        cursor = self._db.connection.cursor()
        cursor.execute('SELECT * FROM alumnos WHERE matricula = ?', (matricula,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        return None

    def find_all(self) -> list[dict]:
        cursor = self._db.connection.cursor()
        cursor.execute('SELECT * FROM alumnos')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def update(self, id: int, nombre: str) -> Optional[dict]:
        cursor = self._db.connection.cursor()
        cursor.execute('UPDATE alumnos SET nombre = ? WHERE id = ?', (nombre, id))
        self._db.connection.commit()

        if cursor.rowcount > 0:
            return self.find_by_id(id)
        return None

    def delete(self, id: int) -> bool:
        cursor = self._db.connection.cursor()
        cursor.execute('DELETE FROM alumnos WHERE id = ?', (id,))
        self._db.connection.commit()
        return cursor.rowcount > 0

    def delete_many(self, ids: list[int]) -> int:
        if len(ids) < 2:
            raise ValueError('Se requieren al menos 2 IDs para eliminar')
        cursor = self._db.connection.cursor()
        placeholders = ','.join('?' * len(ids))
        cursor.execute(f'DELETE FROM alumnos WHERE id IN ({placeholders})', ids)
        self._db.connection.commit()
        return cursor.rowcount
