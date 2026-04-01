import base64
import io

import pypdfium2 as pdfium
from PIL import Image


class ConversionError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message


def _encode_image(image: Image.Image, output_format: str) -> str:
    buffer = io.BytesIO()
    save_format = "PNG" if output_format == "png" else "JPEG"
    image.save(buffer, format=save_format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def convert_pdf_to_images(
    pdf_base64: str,
    output_format: str = "png",
    quality_dpi: int = 300,
) -> list[dict]:
    if not pdf_base64:
        raise ConversionError("PDF_INVALID", "Пустой входной PDF.")

    try:
        pdf_bytes = base64.b64decode(pdf_base64, validate=True)
    except Exception as exc:
        raise ConversionError("PDF_INVALID", "Некорректный формат pdf_base64.") from exc

    try:
        document = pdfium.PdfDocument(pdf_bytes)
    except Exception as exc:
        # pypdfium2 не всегда стабильно отдает тип ошибки, поэтому проверяем текст.
        error_text = str(exc).lower()
        if "password" in error_text or "encrypted" in error_text:
            raise ConversionError(
                "PDF_PASSWORD_REQUIRED", "PDF защищен паролем, требуется пароль."
            ) from exc
        raise ConversionError("PDF_INVALID", "Не удалось прочитать PDF-документ.") from exc

    pages: list[dict] = []
    scale = max(quality_dpi, 300) / 72.0

    try:
        for index in range(len(document)):
            page = document.get_page(index)
            pil_image = page.render(scale=scale).to_pil()
            pages.append(
                {
                    "page_number": index + 1,
                    "format": output_format,
                    "image_data": _encode_image(pil_image, output_format),
                }
            )
    except ConversionError:
        raise
    except Exception as exc:
        raise ConversionError("INTERNAL_ERROR", "Ошибка конвертации PDF.") from exc

    if not pages:
        raise ConversionError("PDF_INVALID", "PDF не содержит страниц для конвертации.")

    return pages
