"""Clase Cliente con validaciones robustas y encapsulación."""
import re

from entidades import Entidad
from excepciones import ClienteInvalidoError


class Cliente(Entidad):
    """Representa un cliente de Software FJ. Los datos son privados y validados."""

    _PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

    def __init__(self, identificador: int, nombre: str, documento: str,
                 correo: str, telefono: str):
        super().__init__(identificador)
        # Se usan los setters para que la validación se aplique desde el inicio
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------- nombre ----------
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        if not all(c.isalpha() or c.isspace() for c in valor):
            raise ClienteInvalidoError("El nombre solo puede contener letras y espacios.")
        self.__nombre = valor.strip().title()

    # ---------- documento ----------
    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.isdigit() or not 6 <= len(valor) <= 10:
            raise ClienteInvalidoError("El documento debe tener entre 6 y 10 dígitos.")
        self.__documento = valor

    # ---------- correo ----------
    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not isinstance(valor, str) or not self._PATRON_CORREO.match(valor):
            raise ClienteInvalidoError(f"Correo electrónico inválido: {valor!r}.")
        self.__correo = valor.lower()

    # ---------- teléfono ----------
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError("El teléfono debe tener exactamente 10 dígitos.")
        self.__telefono = valor

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.nombre} (Doc: {self.documento}, {self.correo})"
