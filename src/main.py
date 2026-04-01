import logging
import os

from fastapi import FastAPI

from src.api.routes import router as conversion_router


def _build_logger() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


_build_logger()

app = FastAPI(
    title=os.getenv("APP_NAME", "pdf-to-images-service"),
    description=(
        "Сервис конвертирует PDF в изображения страниц.\n\n"
        "- `/v1/convert`: принимает JSON с `pdf_base64`, возвращает JSON с `pages[]`.\n"
        "- `/v1/convert/binary`: принимает бинарный PDF, возвращает ZIP с изображениями."
    ),
    version="1.1.0",
    docs_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "PDF to Images API",
        "url": "https://github.com/alex-vakaev/PDF-to-image",
    },
)
app.include_router(conversion_router)


@app.get("/health")
def health():
    return {"status": "ok"}
