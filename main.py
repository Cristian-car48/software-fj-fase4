"""Simulación de 12 operaciones de Software FJ (sin base de datos)."""
from gestor import GestorFJ
from logger import ARCHIVO_LOG, log


def titulo(n, texto):
    print(f"\n--- Operación {n}: {texto}")


def main():
    log.info("===== INICIO DE LA SIMULACIÓN =====")
    fj = GestorFJ()

    titulo(1, "Registro VÁLIDO de cliente")
    ana = fj.registrar_cliente(nombre="ana maria lopez", documento="1085123456",
                               correo="ana@correo.com", telefono="3101234567")

    titulo(2, "Registro INVÁLIDO de cliente (correo y documento incorrectos)")
    fj.registrar_cliente(nombre="Luis Perez", documento="12ab", correo="luis@", telefono="3001112233")

    titulo(3, "Registro INVÁLIDO de cliente (parámetro faltante)")
    fj.registrar_cliente(nombre="Carlos Ruiz", documento="1234567890")

    titulo(4, "Registro VÁLIDO de segundo cliente")
    juan = fj.registrar_cliente(nombre="Juan Torres", documento="987654321",
                                correo="JUAN@mail.com", telefono="3209876543")

    titulo(5, "Creación CORRECTA de los 3 servicios")
    sala = fj.crear_servicio("sala", nombre="Sala Ejecutiva", tarifa_hora=80000, capacidad=10)
    equipo = fj.crear_servicio("equipo", nombre="Portátil Gamer", tarifa_hora=15000, stock=5)
    asesoria = fj.crear_servicio("asesoria", nombre="Asesoría en Python",
                                 tarifa_hora=50000, especialidad="Programación")

    titulo(6, "Creación INCORRECTA de servicios (tarifa negativa y tipo inexistente)")
    fj.crear_servicio("sala", nombre="Sala Fantasma", tarifa_hora=-5, capacidad=4)
    fj.crear_servicio("drone", nombre="Drone", tarifa_hora=1000)

    titulo(7, "Reserva EXITOSA de sala + procesamiento")
    r1 = fj.crear_reserva(ana, sala, 3, asistentes=8)
    fj.procesar_reserva(r1)

    titulo(8, "Reserva FALLIDA (asistentes superan la capacidad)")
    fj.crear_reserva(juan, sala, 2, asistentes=25)

    titulo(9, "Reserva EXITOSA de equipo con descuento del 10 %")
    r2 = fj.crear_reserva(juan, equipo, 4, cantidad=2)
    fj.procesar_reserva(r2, impuesto=0.19, descuento=0.10)

    titulo(10, "Reserva FALLIDA (servicio no disponible)")
    asesoria.disponible = False
    fj.crear_reserva(ana, asesoria, 2, nivel="senior")
    asesoria.disponible = True

    titulo(11, "Reserva de asesoría (nivel inválido) y luego correcta")
    fj.crear_reserva(ana, asesoria, 2, nivel="maestro")
    r3 = fj.crear_reserva(ana, asesoria, 2, nivel="senior")

    titulo(12, "Cancelar y luego intentar procesar / cancelar de nuevo (operaciones no permitidas)")
    fj.cancelar_reserva(r3)
    fj.procesar_reserva(r3)
    fj.cancelar_reserva(r3)
    fj.procesar_reserva(None)

    print("\n--- Demostración de métodos sobrecargados (costos de la sala, 3 h, 8 personas)")
    print("  Sin impuesto  :", sala.calcular_costo(3, asistentes=8))
    print("  Con IVA       :", sala.calcular_costo_con_impuesto(3, asistentes=8))
    print("  IVA + 15% dto :", sala.calcular_costo_con_descuento(3, 0.15, asistentes=8))

    fj.resumen()
    log.info("===== FIN DE LA SIMULACIÓN =====")
    print(f"\nLa aplicación terminó sin interrupciones. Revisa el log en: {ARCHIVO_LOG}")


if __name__ == "__main__":
    main()
