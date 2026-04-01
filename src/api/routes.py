import logging
from uuid import uuid4

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.schemas.conversion import ConversionErrorResponse, ConversionRequest
from src.services.pdf_convert import ConversionError, convert_pdf_to_images

router = APIRouter(prefix="/v1", tags=["conversion"])
logger = logging.getLogger(__name__)


@router.post("/convert")
def convert_pdf(request: ConversionRequest):
    request_id = str(uuid4())
    logger.info("start conversion request_id=%s", request_id)

    try:
        pages = convert_pdf_to_images(
            pdf_base64=request.pdf_base64,
            output_format=request.output_format,
            quality_dpi=request.quality_dpi,
        )
        response = {
            "status": "success",
            "page_count": len(pages),
            "pages": pages,
            "message": "Конвертация завершена успешно.",
            "request_id": request_id,
        }
        logger.info("success conversion request_id=%s pages=%s", request_id, len(pages))
        return response
    except ConversionError as exc:
        logger.warning(
            "conversion error request_id=%s code=%s message=%s",
            request_id,
            exc.error_code,
            exc.message,
        )
        error = ConversionErrorResponse(error_code=exc.error_code, message=exc.message)
        payload = error.model_dump()
        payload["request_id"] = request_id
        return JSONResponse(status_code=400, content=payload)
    except Exception:
        logger.exception("unexpected conversion error request_id=%s", request_id)
        error = ConversionErrorResponse(
            error_code="INTERNAL_ERROR",
            message="Внутренняя ошибка сервиса.",
        )
        payload = error.model_dump()
        payload["request_id"] = request_id
        return JSONResponse(status_code=500, content=payload)
