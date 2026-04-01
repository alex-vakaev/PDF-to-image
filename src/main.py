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

app = FastAPI(title=os.getenv("APP_NAME", "pdf-to-images-service"))
app.include_router(conversion_router)


@app.get("/health")
def health():
    return {"status": "ok"}
