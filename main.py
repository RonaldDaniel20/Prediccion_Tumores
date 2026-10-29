from fastapi import FastAPI
from routers import healths, modelo
from fastapi.middleware.cors import CORSMiddleware
from core.config_logging import configure_logging
from middlewares.logging_middleware import RequestLoggingMiddleware
from config import get_settings



configure_logging()
URL_FRONT = get_settings().FRONT_URL
app = FastAPI()

print("URL_FRONT", URL_FRONT)
origins = [
    URL_FRONT
]

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(healths.router)
app.include_router(modelo.router)


@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "API is running"
    }

