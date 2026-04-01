# Data Model: Конвертация PDF в изображения страниц

## Entity: ConversionRequest

- `request_id`: string, уникальный идентификатор запроса
- `input_pdf`: binary/string, входной PDF в теле запроса
- `output_format`: enum(`png`, `jpeg`), по умолчанию `png`
- `quality_dpi`: integer, минимум `300` для сценария чертежей

Validation rules:
- PDF обязателен и должен быть корректно читаем.
- `output_format` ограничен `png` или `jpeg`.
- Если задан `quality_dpi`, он не может быть меньше `300`.

## Entity: PageImage

- `page_number`: integer, начиная с 1
- `format`: enum(`png`, `jpeg`)
- `image_data`: string (base64), содержимое изображения

Validation rules:
- `page_number` уникален в рамках одного ответа.
- Порядок в массиве соответствует порядку страниц PDF.

## Entity: ConversionResponse

- `status`: enum(`success`, `error`)
- `pages`: array<PageImage>, присутствует при `success`
- `page_count`: integer, количество страниц
- `message`: string, человекочитаемое описание результата
- `error_code`: string, присутствует при `error`

State transitions:
- `received` -> `processing` -> `success`
- `received` -> `processing` -> `error`

Consistency rules:
- При `success`: `page_count == len(pages)`.
- При `error`: `pages` пустой или отсутствует, указан `error_code`.

