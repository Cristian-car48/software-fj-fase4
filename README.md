# Software FJ – Sistema de Gestión de Clientes, Servicios y Reservas
Curso Programación 213023 – UNAD – Fase 4 (POO + manejo avanzado de excepciones). Sin bases de datos.

## Ejecución
    python main.py        # Python 3.9+

## Estructura
| Archivo | Contenido |
|---|---|
| entidades.py | Clase abstracta `Entidad` |
| cliente.py | `Cliente` (encapsulación + validaciones) |
| servicios.py | `Servicio` (abstracta) → `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| reserva.py | `Reserva` (confirmar, cancelar, procesar) |
| excepciones.py | Excepciones personalizadas |
| logger.py | Archivo `logs/software_fj.log` |
| gestor.py | Listas internas y operaciones controladas |
| main.py | Simulación de 12 operaciones |

## Requisitos cubiertos
- Abstracción, herencia, polimorfismo, encapsulación.
- Sobrecarga simulada: `calcular_costo`, `calcular_costo_con_impuesto`, `calcular_costo_con_descuento`.
- try/except, try/except/else, try/except/finally y encadenamiento (`raise ... from`).
- Logs de errores y eventos; el programa nunca se detiene.
