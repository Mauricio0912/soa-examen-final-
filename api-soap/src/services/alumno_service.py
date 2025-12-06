from src.repositories import AlumnoRepository
from src.database import get_database


class AlumnoService:

    def __init__(self):
        self._repo = AlumnoRepository(get_database())

    def crear_alumno(self, nombre: str) -> dict:
        return self._repo.create(nombre)

    def obtener_alumno(self, id: int) -> dict | None:
        return self._repo.find_by_id(id)

    def obtener_por_matricula(self, matricula: str) -> dict | None:
        return self._repo.find_by_matricula(matricula)

    def listar_alumnos(self) -> list[dict]:
        return self._repo.find_all()

    def actualizar_alumno(self, id: int, nombre: str) -> dict | None:
        return self._repo.update(id, nombre)

    def eliminar_alumno(self, id: int) -> bool:
        return self._repo.delete(id)

    def eliminar_alumnos(self, ids: list[int]) -> int:
        return self._repo.delete_many(ids)
