"""Configuración del archivo de logs (errores y eventos relevantes)."""
import logging
import os

# Carpeta y archivo donde se guardan los registros
RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")


def obtener_logger() -> logging.Logger:
    """Devuelve un logger único que escribe en logs/software_fj.log."""
    os.makedirs(RUTA_LOGS, exist_ok=True)  # crea la carpeta si no existe
    logger = logging.getLogger("software_fj")
    if not logger.handlers:  # evita duplicar handlers si se llama varias veces
        logger.setLevel(logging.INFO)
        manejador = logging.FileHandler(ARCHIVO_LOG, mode="a", encoding="utf-8")
        manejador.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        )
        logger.addHandler(manejador)
    return logger


log = obtener_logger()
