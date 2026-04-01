# PDF to Images API

Простой FastAPI-сервис для конвертации PDF в изображения страниц с акцентом на читаемость (минимум эквивалент 300 DPI).

## Возможности

- Конвертация PDF из `base64` в JSON с массивом изображений (`/v1/convert`)
- Конвертация бинарного PDF в ZIP с бинарными PNG/JPEG (`/v1/convert/binary`)
- Обработка ошибок с `error_code` и `request_id`
- Swagger UI: `/swagger`
- ReDoc: `/redoc`

## Требования

- Python 3.11+

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

После запуска:

- Health: `http://127.0.0.1:8000/health`
- Swagger: `http://127.0.0.1:8000/swagger`
- OpenAPI: `http://127.0.0.1:8000/openapi.json`

## API

### 1) JSON endpoint

`POST /v1/convert`

Пример тела:

```json
{
  "pdf_base64": "<BASE64_PDF>",
  "output_format": "png",
  "quality_dpi": 300
}
```

### 2) Binary endpoint

`POST /v1/convert/binary`

Формат: `multipart/form-data`

- `pdf_file` — файл PDF
- `output_format` — `png` или `jpeg` (по умолчанию `png`)
- `quality_dpi` — минимум `300`

Пример:

```bash
curl -X POST "http://127.0.0.1:8000/v1/convert/binary" \
  -F "pdf_file=@./sample.pdf" \
  -F "output_format=png" \
  -F "quality_dpi=300" \
  -o pages.zip
```

## Postman

Коллекция лежит в файле:

- `postman/pdf-to-images.postman_collection.json`

## Ошибки

Основные коды:

- `PDF_INVALID`
- `PDF_PASSWORD_REQUIRED`
- `INTERNAL_ERROR`

Во всех ответах об ошибке возвращается `request_id` для трассировки.
