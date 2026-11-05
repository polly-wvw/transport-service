# Transport Maintenance Service

REST API для обработки заявок на техническое обслуживание подвижного состава.

## Запуск

```bash
docker-compose up -d

Swagger UI: http://localhost:8000/docs

Эндпоинты
Метод	            Путь	                Описание
GET	                /api/v1/routes/	        Список заявок
GET	                /api/v1/routes/{id}	    Заявка по ID
POST	            /api/v1/routes/	        Создать заявку
PATCH	            /api/v1/routes/{id}	    Обновить заявку
DELETE	            /api/v1/routes/{id}	    Удалить заявку

