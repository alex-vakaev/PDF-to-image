from typing import Literal

from pydantic import BaseModel, Field


class ConversionRequest(BaseModel):
    pdf_base64: str = Field(..., min_length=1)
    output_format: Literal["png", "jpeg"] = "png"
    quality_dpi: int = Field(default=300, ge=300)


class PageImage(BaseModel):
    page_number: int = Field(..., ge=1)
    format: Literal["png", "jpeg"]
    image_data: str


class ConversionSuccessResponse(BaseModel):
    status: Literal["success"] = "success"
    page_count: int = Field(..., ge=1)
    pages: list[PageImage]
    message: str


class ConversionErrorResponse(BaseModel):
    status: Literal["error"] = "error"
    error_code: Literal[
        "INPUT_NOT_FOUND",
        "PDF_INVALID",
        "PDF_PASSWORD_REQUIRED",
        "INTERNAL_ERROR",
    ]
    message: str
