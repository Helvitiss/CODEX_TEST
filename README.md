# Food Delivery Monorepo

Монорепозиторий с:
- **Backend**: FastAPI + async SQLAlchemy
- **Frontend**: React + Vite

## Требования

- Docker
- Docker Compose Plugin (`docker compose`)

## Запуск через Docker Compose

```bash
docker compose up --build
```

После старта:
- Backend API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

Остановка:

```bash
docker compose down
```

Остановка с удалением томов/артефактов контейнеров:

```bash
docker compose down --volumes --remove-orphans
```

## Сидирование данных в Docker

```bash
docker compose exec backend python -m scripts.seed
```

Сидер создаёт:
- минимум 6 категорий
- минимум 30 блюд
- fake `image_path` для блюд

## Загрузка изображений блюд

Эндпоинт (только admin):

```http
POST /admin/dishes/{dish_id}/image
Content-Type: multipart/form-data
```

Пример:

```bash
curl -X POST "http://localhost:8000/admin/dishes/1/image" \
  -H "Authorization: Bearer <ADMIN_JWT>" \
  -F "image=@/path/to/file.webp"
```

Файлы сохраняются локально в:
- `backend/media/dishes`

И доступны по URL:
- `/media/dishes/<filename>`

## CORS (frontend -> backend)

По умолчанию backend разрешает origin:
- `http://localhost:5173`
- `http://127.0.0.1:5173`

Переопределение через env:

```env
APP_CORS_ALLOW_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Переменные и сборка

- Backend собирается из `Dockerfile.backend`
- Frontend собирается из `Dockerfile.frontend`
- Базовый URL API для frontend задаётся build-аргументом `VITE_API_URL` в `docker-compose.yml`

## Полезные команды

Проверить конфигурацию compose:

```bash
docker compose config
```

Пересобрать только frontend:

```bash
docker compose build frontend
```

Пересобрать только backend:

```bash
docker compose build backend
```
