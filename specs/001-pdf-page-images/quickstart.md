# Quickstart: PDF to Images Service

## 1) Install dependencies

```bash
pip install -r requirements.txt
```

## 2) Run service

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## 3) Send convert request

### Bash (Linux/macOS)

```bash
curl -X POST "http://localhost:8000/v1/convert" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_base64": "<BASE64_PDF>",
    "output_format": "png",
    "quality_dpi": 300
  }'
```

### PowerShell (Windows)

```powershell
$body = @{
  pdf_base64 = "<BASE64_PDF>"
  output_format = "png"
  quality_dpi = 300
} | ConvertTo-Json

Invoke-RestMethod -Method POST `
  -Uri "http://localhost:8000/v1/convert" `
  -ContentType "application/json" `
  -Body $body
```

### Binary PDF -> Binary PNG (separate endpoint)

```bash
curl -X POST "http://localhost:8000/v1/convert/binary" \
  -F "pdf_file=@./sample.pdf" \
  -F "output_format=png" \
  -F "quality_dpi=300" \
  -o pages.zip
```

Содержимое `pages.zip`: `page-0001.png`, `page-0002.png`, ...

## 4) Validate response

- `status` должен быть `success`
- `page_count` должен совпадать с количеством страниц PDF
- `pages` должен содержать изображения всех страниц в порядке исходного документа
- `request_id` должен присутствовать в ответе

### Success response example

```json
{
  "status": "success",
  "page_count": 2,
  "pages": [
    {
      "page_number": 1,
      "format": "png",
      "image_data": "<BASE64_IMAGE>"
    },
    {
      "page_number": 2,
      "format": "png",
      "image_data": "<BASE64_IMAGE>"
    }
  ],
  "message": "Конвертация завершена успешно.",
  "request_id": "6d8f3f4f-35d1-4a91-bac4-3a9ff9d6a86c"
}
```

## 5) Error checks

- Для PDF с паролем ожидается `error_code=PDF_PASSWORD_REQUIRED`
- Для невалидного PDF ожидается `error_code=PDF_INVALID`
- Для ошибок должен присутствовать `request_id`

