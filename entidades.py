"""Clase abstracta base para las entidades generales del sistema."""
from abc import ABC, abstractmethod


class Entidad(ABC):
    """Abstracción de cualquier entidad con identificador (cliente, servicio, reserva)."""

    def __init__(self, identificador: int):
        self._id = identificador  # atributo protegido (encapsulación)

    @property
    def id(self) -> int:
        """Solo lectura: el id no se modifica una vez creado."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad debe describirse a sí misma (polimorfismo)."""

    def __str__(self) -> str:
        return self.describir()
