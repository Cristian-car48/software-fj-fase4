"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, lo que permite capturar cualquier error
propio del sistema con un único `except SoftwareFJError`.
"""


class SoftwareFJError(Exception):
    """Excepción base de la aplicación."""


class ClienteInvalidoError(SoftwareFJError):
    """Datos de cliente inválidos (nombre, documento, correo, teléfono)."""


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parámetro obligatorio en una operación."""


class ServicioInvalidoError(SoftwareFJError):
    """Parámetros inválidos al crear o usar un servicio."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""


class ReservaError(SoftwareFJError):
    """Error general en la gestión de una reserva."""


class OperacionNoPermitidaError(ReservaError):
    """Operación no permitida según el estado actual de la reserva."""


class CalculoInconsistenteError(SoftwareFJError):
    """Cálculo de costos con resultados inconsistentes."""
