from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Alumno:
    id: Optional[int] = None
    matricula: Optional[str] = None
    nombre: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Alumno':
        return cls(
            id=data.get('id'),
            matricula=data.get('matricula'),
            nombre=data.get('nombre')
        )

    def to_dict(self) -> dict:
        return asdict(self)
