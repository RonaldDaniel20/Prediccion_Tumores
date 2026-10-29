from fastapi import FastAPI
from routers import healths, modelo
from fastapi.middleware.cors import CORSMiddleware
from core.config_logging import configure_logging
from middlewares.logging_middleware import RequestLoggingMiddleware



configure_logging()
app = FastAPI()

origins = [
    "http://127.0.0.1:4200"
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

