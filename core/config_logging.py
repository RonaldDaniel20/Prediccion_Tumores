import os 
import logging
import sys
from config import get_settings

def get_log_level() -> int:

    env = get_settings().ENVIRONMENT  
    nombre_nivel = get_settings().LOG_LEVEL.upper()

    if nombre_nivel:
        return getattr(logging, nombre_nivel, logging.INFO)
    
    env_defecto = {
        "development": logging.DEBUG,
        "production": logging.INFO
    }

    return env_defecto.get(env, logging.INFO)

def configure_logging():

    nivel = get_log_level()
    
    internal_configs = {
        "middlewares": logging.INFO,
        "services": logging.DEBUG
    }

    formato = logging.Formatter(
        '{"timestamp": "%(asctime)s","entorno":"%(entorno)s", "level": "%(levelname)s", "logger": "%(name)s", "request_id": "%(tags)s", "message": "%(message)s"',
        datefmt="%Y-%m-%dT%H:%M:%SZ"
    )

    for logger_name, level in internal_configs.items():
        prioridad = max(nivel, level)
        logger_modulo = logging.getLogger(logger_name)
        logger_modulo.setLevel(prioridad)

        if not logger_modulo.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formato)
            logger_modulo.addHandler(handler)
        




    

