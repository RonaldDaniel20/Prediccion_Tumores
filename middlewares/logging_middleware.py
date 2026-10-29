import logging
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from config import get_settings

logger = logging.getLogger(__name__)

entorno = get_settings().ENVIRONMENT

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))

        registros_python = logging.getLogRecordFactory()
        def inyectar_registro(*args, **kwargs):
            registro_logging = registros_python(*args, **kwargs)
            registro_logging.tags = request_id
            registro_logging.entorno = entorno
            return registro_logging
        
        logging.setLogRecordFactory(inyectar_registro)

        tiempo_inicio = time.time()

        response = await call_next(request)

        response.headers['X-Request-ID'] = request_id

        return response
