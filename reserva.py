"""Clase Reserva: integra cliente, servicio, duración y estado."""
from cliente import Cliente
from entidades import Entidad
from excepciones import (OperacionNoPermitidaError, ReservaError,
                         ServicioNoDisponibleError, SoftwareFJError)
from logger import log
from servicios import Servicio

PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"


class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    def __init__(self, identificador: int, cliente: Cliente, servicio: Servicio,
                 horas: float, **parametros):
        super().__init__(identificador)
        # Validaciones de integridad (si algo falla, se encadena la causa original)
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva requiere un servicio válido.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")
        try:
            servicio.validar_parametros(**parametros)
            if not isinstance(horas, (int, float)) or horas <= 0:
                raise ValueError("La duración debe ser positiva.")
        except (SoftwareFJError, ValueError) as error:
            # Encadenamiento de excepciones: 'from error' conserva la causa original
            raise ReservaError("Intento de reserva incorrecto.") from error
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._parametros = parametros
        self._estado = PENDIENTE
        self._costo = None

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self) -> None:
        """Confirma la reserva; solo es posible si está PENDIENTE."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError("El servicio dejó de estar disponible.")
        self._estado = CONFIRMADA
        log.info(f"Reserva #{self.id} confirmada.")

    def cancelar(self) -> None:
        """Cancela la reserva; no se puede cancelar una ya procesada o cancelada."""
        if self._estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado}.")
        self._estado = CANCELADA
        log.info(f"Reserva #{self.id} cancelada.")

    def procesar(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """Procesa la reserva (calcula el costo final) usando try/except/else/finally."""
        try:
            if self._estado != CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesan reservas CONFIRMADAS (actual: {self._estado}).")
            total = self._servicio.calcular_costo(
                self._horas, impuesto=impuesto, descuento=descuento, **self._parametros)
        except SoftwareFJError as error:
            log.error(f"Reserva #{self.id}: fallo al procesar -> {error}")
            raise  # se relanza para que el gestor decida qué hacer
        else:
            # Solo se ejecuta si NO hubo excepción
            self._costo = total
            self._estado = PROCESADA
            log.info(f"Reserva #{self.id} procesada. Total: ${total:,.2f}")
            return total
        finally:
            # Se ejecuta siempre, haya o no error
            log.info(f"Reserva #{self.id}: intento de procesamiento finalizado "
                     f"(estado={self._estado}).")

    def describir(self) -> str:
        costo = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (f"Reserva #{self.id} | {self._cliente.nombre} -> {self._servicio.nombre} | "
                f"{self._horas} h | {self._estado} | Costo: {costo}")
