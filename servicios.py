"""Clase abstracta Servicio y tres servicios especializados (herencia + polimorfismo)."""
from abc import abstractmethod

from entidades import Entidad
from excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                         ServicioInvalidoError)

IVA = 0.19  # impuesto por defecto (19 %)


class Servicio(Entidad):
    """Servicio genérico ofrecido por Software FJ."""

    def __init__(self, identificador: int, nombre: str, tarifa_hora: float,
                 disponible: bool = True):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio necesita un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser un número positivo.")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    # ---------- métodos abstractos (se sobrescriben en cada servicio) ----------
    @abstractmethod
    def validar_parametros(self, **parametros) -> None:
        """Valida los parámetros específicos de la reserva de este servicio."""

    @abstractmethod
    def costo_base(self, horas: float, **parametros) -> float:
        """Costo base (sin impuestos ni descuentos) según el tipo de servicio."""

    # ---------- métodos sobrecargados de cálculo de costos ----------
    # Python no tiene sobrecarga nativa: se simula con parámetros opcionales
    # y con variantes nombradas del mismo cálculo.
    def calcular_costo(self, horas: float, impuesto: float = 0.0,
                       descuento: float = 0.0, **parametros) -> float:
        """Variante general: costo base + impuesto - descuento (porcentajes 0-1)."""
        if horas is None:
            raise ParametroFaltanteError("La duración (horas) es obligatoria.")
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ServicioInvalidoError("La duración debe ser un número positivo de horas.")
        if not (0 <= impuesto <= 1 and 0 <= descuento <= 1):
            raise CalculoInconsistenteError("Impuesto y descuento deben estar entre 0 y 1.")
        base = self.costo_base(horas, **parametros)
        total = base * (1 + impuesto) * (1 - descuento)
        if total < 0:
            raise CalculoInconsistenteError("El costo calculado es negativo.")
        return round(total, 2)

    def calcular_costo_con_impuesto(self, horas: float, **parametros) -> float:
        """Variante 2: aplica el IVA por defecto."""
        return self.calcular_costo(horas, impuesto=IVA, **parametros)

    def calcular_costo_con_descuento(self, horas: float, descuento: float,
                                     **parametros) -> float:
        """Variante 3: aplica IVA y un descuento."""
        return self.calcular_costo(horas, impuesto=IVA, descuento=descuento, **parametros)

    def describir(self) -> str:
        estado = "disponible" if self._disponible else "NO disponible"
        return f"[{self.__class__.__name__}] {self._nombre} - ${self._tarifa_hora:,.0f}/h ({estado})"


class ReservaSala(Servicio):
    """Reserva de salas: depende de la capacidad y de los asistentes."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad: int, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, **parametros) -> None:
        asistentes = parametros.get("asistentes")
        if asistentes is None:
            raise ParametroFaltanteError("Falta el parámetro 'asistentes' para la sala.")
        if not isinstance(asistentes, int) or not 0 < asistentes <= self._capacidad:
            raise ServicioInvalidoError(
                f"Asistentes inválidos ({asistentes}); capacidad máxima: {self._capacidad}.")

    def costo_base(self, horas, **parametros) -> float:
        self.validar_parametros(**parametros)
        return self._tarifa_hora * horas

    def describir(self) -> str:
        return super().describir() + f" | Capacidad: {self._capacidad} personas"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: el costo depende de la cantidad de unidades."""

    def __init__(self, identificador, nombre, tarifa_hora, stock: int, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(stock, int) or stock <= 0:
            raise ServicioInvalidoError("El stock debe ser un entero positivo.")
        self._stock = stock

    def validar_parametros(self, **parametros) -> None:
        cantidad = parametros.get("cantidad")
        if cantidad is None:
            raise ParametroFaltanteError("Falta el parámetro 'cantidad' del equipo.")
        if not isinstance(cantidad, int) or not 0 < cantidad <= self._stock:
            raise ServicioInvalidoError(
                f"Cantidad inválida ({cantidad}); stock disponible: {self._stock}.")

    def costo_base(self, horas, **parametros) -> float:
        self.validar_parametros(**parametros)
        return self._tarifa_hora * horas * parametros["cantidad"]

    def describir(self) -> str:
        return super().describir() + f" | Stock: {self._stock} unidades"


class AsesoriaEspecializada(Servicio):
    """Asesoría: la tarifa se multiplica según el nivel del asesor."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, identificador, nombre, tarifa_hora, especialidad: str, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La asesoría requiere una especialidad.")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, **parametros) -> None:
        nivel = parametros.get("nivel")
        if nivel is None:
            raise ParametroFaltanteError("Falta el parámetro 'nivel' del asesor.")
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel '{nivel}' inválido. Opciones: {list(self.NIVELES)}.")

    def costo_base(self, horas, **parametros) -> float:
        self.validar_parametros(**parametros)
        return self._tarifa_hora * horas * self.NIVELES[parametros["nivel"]]

    def describir(self) -> str:
        return super().describir() + f" | Especialidad: {self._especialidad}"
