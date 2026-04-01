import logging
import io
import zipfile
from uuid import uuid4

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse, Response

from src.schemas.conversion import ConversionErrorResponse, ConversionRequest
from src.services.pdf_convert import (
    ConversionError,
    convert_pdf_bytes_to_images,
    convert_pdf_to_images,
)

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


@router.post("/convert/binary")
async def convert_pdf_binary(
    pdf_file: UploadFile = File(...),
    output_format: str = Form("png"),
    quality_dpi: int = Form(300),
):
    request_id = str(uuid4())
    logger.info("start binary conversion request_id=%s", request_id)

    if output_format not in {"png", "jpeg"}:
        error = ConversionErrorResponse(
            error_code="PDF_INVALID",
            message="Допустимые output_format: png или jpeg.",
        )
        payload = error.model_dump()
        payload["request_id"] = request_id
        return JSONResponse(status_code=400, content=payload)

    try:
        pdf_bytes = await pdf_file.read()
        pages = convert_pdf_bytes_to_images(
            pdf_bytes=pdf_bytes,
            output_format=output_format,
            quality_dpi=quality_dpi,
        )

        # Отдаем бинарный результат всех страниц одним архивом.
        zip_buffer = io.BytesIO()
        extension = "png" if output_format == "png" else "jpg"
        with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for page in pages:
                file_name = f"page-{page['page_number']:04d}.{extension}"
                zf.writestr(file_name, page["image_bytes"])

        logger.info(
            "success binary conversion request_id=%s pages=%s",
            request_id,
            len(pages),
        )
        headers = {
            "Content-Disposition": 'attachment; filename="pages.zip"',
            "X-Request-Id": request_id,
        }
        return Response(
            content=zip_buffer.getvalue(),
            media_type="application/zip",
            headers=headers,
        )
    except ConversionError as exc:
        logger.warning(
            "binary conversion error request_id=%s code=%s message=%s",
            request_id,
            exc.error_code,
            exc.message,
        )
        error = ConversionErrorResponse(error_code=exc.error_code, message=exc.message)
        payload = error.model_dump()
        payload["request_id"] = request_id
        return JSONResponse(status_code=400, content=payload)
    except Exception:
        logger.exception("unexpected binary conversion error request_id=%s", request_id)
        error = ConversionErrorResponse(
            error_code="INTERNAL_ERROR",
            message="Внутренняя ошибка сервиса.",
        )
        payload = error.model_dump()
        payload["request_id"] = request_id
        return JSONResponse(status_code=500, content=payload)
