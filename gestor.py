"""Gestor principal: administra listas internas de clientes, servicios y reservas."""
from cliente import Cliente
from excepciones import SoftwareFJError, ReservaError
from logger import log
from reserva import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio

# Fábrica: asocia el nombre del tipo con su clase (facilita la extensión)
TIPOS_SERVICIO = {"sala": ReservaSala, "equipo": AlquilerEquipo, "asesoria": AsesoriaEspecializada}


class GestorFJ:
    """Orquesta las operaciones y garantiza que el sistema nunca se detenga."""

    def __init__(self):
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []

    def registrar_cliente(self, **datos):
        """Crea y almacena un cliente. Devuelve None si los datos son inválidos."""
        try:
            cliente = Cliente(len(self._clientes) + 1, **datos)
        except SoftwareFJError as error:
            log.error(f"Registro de cliente fallido: {error}")
            print(f"  ✗ Cliente NO registrado: {error}")
            return None
        except TypeError as error:  # parámetros faltantes o sobrantes
            log.error(f"Registro de cliente con parámetros incorrectos: {error}")
            print(f"  ✗ Cliente NO registrado (parámetros): {error}")
            return None
        else:
            self._clientes.append(cliente)
            log.info(f"Cliente registrado: {cliente.describir()}")
            print(f"  ✓ {cliente}")
            return cliente

    def crear_servicio(self, tipo: str, **datos):
        """Crea y almacena un servicio del tipo indicado."""
        try:
            clase = TIPOS_SERVICIO.get(tipo)
            if clase is None:
                raise ReservaError(f"Tipo de servicio desconocido: '{tipo}'.")
            servicio = clase(len(self._servicios) + 1, **datos)
        except (SoftwareFJError, TypeError) as error:
            log.error(f"Creación de servicio fallida ({tipo}): {error}")
            print(f"  ✗ Servicio NO creado: {error}")
            return None
        else:
            self._servicios.append(servicio)
            log.info(f"Servicio creado: {servicio.describir()}")
            print(f"  ✓ {servicio}")
            return servicio

    def crear_reserva(self, cliente, servicio, horas, confirmar=True, **parametros):
        """Crea una reserva y, opcionalmente, la confirma."""
        try:
            reserva = Reserva(len(self._reservas) + 1, cliente, servicio, horas, **parametros)
            if confirmar:
                reserva.confirmar()
        except SoftwareFJError as error:
            causa = f" (causa: {error.__cause__})" if error.__cause__ else ""
            log.error(f"Reserva fallida: {error}{causa}")
            print(f"  ✗ Reserva NO creada: {error}{causa}")
            return None
        else:
            self._reservas.append(reserva)
            print(f"  ✓ {reserva}")
            return reserva
        finally:
            log.info("Intento de creación de reserva finalizado.")

    def procesar_reserva(self, reserva, **kwargs):
        """Procesa una reserva sin dejar que un error detenga el programa."""
        try:
            total = reserva.procesar(**kwargs)
        except SoftwareFJError as error:
            print(f"  ✗ No se pudo procesar: {error}")
            return None
        except AttributeError as error:  # reserva = None
            log.error(f"Procesamiento sobre reserva inexistente: {error}")
            print("  ✗ No hay reserva para procesar.")
            return None
        print(f"  ✓ Procesada. Total: ${total:,.2f}")
        return total

    def cancelar_reserva(self, reserva):
        """Cancela una reserva controlando errores."""
        try:
            reserva.cancelar()
        except SoftwareFJError as error:
            log.error(f"Cancelación fallida: {error}")
            print(f"  ✗ No se pudo cancelar: {error}")
        else:
            print(f"  ✓ Cancelada: {reserva}")

    def resumen(self):
        print(f"\nRESUMEN -> Clientes: {len(self._clientes)} | "
              f"Servicios: {len(self._servicios)} | Reservas: {len(self._reservas)}")
        for r in self._reservas:
            print("  ", r)
