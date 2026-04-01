# Tasks: Конвертация PDF в изображения страниц

**Input**: Design documents from `C:\Users\user\pdf-to-img\specs\001-pdf-page-images\`
**Prerequisites**: `plan.md` (required), `spec.md` (required), `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Явный TDD-запрос в спецификации отсутствует, поэтому отдельные test-first задачи не добавлены.

**Organization**: Задачи сгруппированы по user story для независимой реализации и проверки.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Можно выполнять параллельно (разные файлы, нет незавершенных зависимостей)
- **[Story]**: Привязка к user story (`[US1]`, `[US2]`, `[US3]`)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Инициализация каркаса сервиса и зависимостей

- [X] T001 Создать каркас сервиса и каталогов в `src/main.py`, `src/api/routes.py`, `src/services/pdf_convert.py`, `src/schemas/conversion.py`
- [X] T002 Добавить зависимости сервиса в `requirements.txt`
- [X] T003 [P] Добавить шаблон конфигурации в `.env.example`
- [X] T004 [P] Настроить базовый FastAPI bootstrap в `src/main.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Общая инфраструктура, блокирующая реализацию всех user stories

**⚠️ CRITICAL**: До завершения этой фазы нельзя полноценно реализовывать user stories

- [X] T005 Создать pydantic-схемы запроса/ответа в `src/schemas/conversion.py`
- [X] T006 [P] Реализовать единый формат ошибок и `error_code` в `src/api/routes.py`
- [X] T007 [P] Реализовать сервисную заготовку конвертации и интерфейс методов в `src/services/pdf_convert.py`
- [X] T008 Подключить endpoint `POST /v1/convert` к сервисному слою в `src/api/routes.py` и `src/main.py`
- [X] T009 Добавить базовое логирование обработки запроса в `src/main.py`

**Checkpoint**: Основа готова, можно переходить к задачам user stories

---

## Phase 3: User Story 1 - Разделение PDF по страницам (Priority: P1) 🎯 MVP

**Goal**: Принять PDF в запросе и вернуть JSON с массивом изображений страниц в правильном порядке

**Independent Test**: Отправить PDF на 3-5 страниц и проверить, что в ответе `page_count` равен числу страниц, а `pages[]` содержит все страницы в исходном порядке

### Implementation for User Story 1

- [X] T010 [US1] Реализовать декодирование и валидацию входного `pdf_base64` в `src/services/pdf_convert.py`
- [X] T011 [US1] Реализовать конвертацию всех страниц PDF в изображения в `src/services/pdf_convert.py`
- [X] T012 [US1] Реализовать формирование массива `pages[]` с `page_number` и `image_data` в `src/services/pdf_convert.py`
- [X] T013 [US1] Реализовать успешный JSON-ответ (`status`, `page_count`, `pages`, `message`) в `src/api/routes.py`
- [X] T014 [US1] Добавить обработку неверного `pdf_base64` и невалидного PDF (`PDF_INVALID`) в `src/api/routes.py`

**Checkpoint**: User Story 1 полностью рабочая и проверяется отдельно

---

## Phase 4: User Story 2 - Высокая читаемость чертежей (Priority: P2)

**Goal**: Обеспечить качество конвертации не ниже эквивалента 300 DPI для мелких элементов

**Independent Test**: Обработать контрольный PDF с мелкими надписями/тонкими линиями и проверить, что результат читаем при рабочем увеличении

### Implementation for User Story 2

- [X] T015 [US2] Реализовать параметр `quality_dpi` с минимумом 300 в `src/schemas/conversion.py`
- [X] T016 [US2] Применить `quality_dpi` к рендерингу страниц в `src/services/pdf_convert.py`
- [X] T017 [P] [US2] Реализовать выбор формата `output_format` (`png` default, `jpeg` optional) в `src/services/pdf_convert.py`
- [X] T018 [US2] Обновить сериализацию `PageImage.format` в ответе в `src/services/pdf_convert.py`
- [X] T019 [US2] Добавить проверку недопустимого `quality_dpi` и форматную валидацию запроса в `src/api/routes.py`

**Checkpoint**: User Story 2 работает независимо и не ломает US1

---

## Phase 5: User Story 3 - Понятные ошибки и повторный запуск (Priority: P3)

**Goal**: Возвращать понятные ошибки для ключевых негативных сценариев без частично успешного результата

**Independent Test**: Передать некорректный PDF и password-protected PDF, убедиться в корректных `status=error` и `error_code`

### Implementation for User Story 3

- [X] T020 [US3] Реализовать обработку password-protected PDF с `error_code=PDF_PASSWORD_REQUIRED` в `src/services/pdf_convert.py`
- [X] T021 [US3] Реализовать обработку общего сбоя конвертации с `error_code=INTERNAL_ERROR` в `src/api/routes.py`
- [X] T022 [P] [US3] Нормализовать тексты ошибок для клиента в `src/api/routes.py`
- [X] T023 [US3] Гарантировать отсутствие частично успешного ответа при ошибках в `src/services/pdf_convert.py`
- [X] T024 [US3] Логировать ошибки конвертации с `request_id` в `src/main.py` и `src/api/routes.py`

**Checkpoint**: Все user stories реализованы и независимы для валидации

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Финальная шлифовка и проверка целостности

- [X] T025 [P] Синхронизировать примеры запросов/ответов в `specs/001-pdf-page-images/quickstart.md`
- [X] T026 Обновить API-контракт под фактические поля ответа в `specs/001-pdf-page-images/contracts/conversion-api.yaml`
- [X] T027 Пройти end-to-end сценарий по `specs/001-pdf-page-images/quickstart.md` и зафиксировать результат в `specs/001-pdf-page-images/research.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: без зависимостей
- **Phase 2 (Foundational)**: зависит от Phase 1, блокирует user stories
- **Phase 3-5 (User Stories)**: зависят от завершения Phase 2
- **Phase 6 (Polish)**: после завершения выбранных user stories

### User Story Dependencies

- **US1 (P1)**: стартует сразу после Foundational, MVP
- **US2 (P2)**: стартует после Foundational, использует инфраструктуру US1
- **US3 (P3)**: стартует после Foundational, может выполняться параллельно с US2 при готовом endpoint-каркасе

### Parallel Opportunities

- **Setup**: `T003`, `T004` параллельно после `T001-T002`
- **Foundational**: `T006` и `T007` параллельно после `T005`
- **US2**: `T017` параллельно с `T016`
- **US3**: `T022` параллельно с `T021`
- **Polish**: `T025` параллельно с `T026`

---

## Parallel Example: User Story 2

```bash
Task: "T016 [US2] Применить quality_dpi к рендерингу в src/services/pdf_convert.py"
Task: "T017 [P] [US2] Реализовать выбор output_format в src/services/pdf_convert.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Завершить Phase 1 и Phase 2
2. Реализовать только Phase 3 (US1)
3. Выполнить независимую проверку US1 по критерию `page_count/pages[]`
4. Показать MVP

### Incremental Delivery

1. Добавить US1 (MVP)
2. Добавить US2 (качество и формат)
3. Добавить US3 (надежные ошибки)
4. Выполнить Phase 6

### Parallel Team Strategy

1. Один разработчик закрывает Phase 1-2
2. После foundation:
   - Разработчик A: US1
   - Разработчик B: US2
   - Разработчик C: US3

---

## Notes

- Все задачи соответствуют формату `- [ ] Txxx ... путь_к_файлу`
- `[USx]` используется только в фазах user stories
- `[P]` отмечен только для реально параллельных задач
