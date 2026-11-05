from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from app.repository import repository
from app.schemas import (
    ServiceRequest,
    ServiceRequestCreate,
    ServiceRequestUpdate,
)

app = FastAPI(
    title="Transport Maintenance Service",
    version="1.0.0",
    description=(
        "REST API для обработки заявок на техническое обслуживание "
        "подвижного состава. Сущность: ServiceRequest (Заявка на ТО)."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get(
    "/api/v1/routes/",
    response_model=list[ServiceRequest],
    status_code=status.HTTP_200_OK,
    tags=["Service Requests"],
    summary="Получить список всех заявок",
)
def list_requests() -> list[ServiceRequest]:
    return repository.list()


@app.get(
    "/api/v1/routes/{request_id}",
    response_model=ServiceRequest,
    status_code=status.HTTP_200_OK,
    tags=["Service Requests"],
    summary="Получить заявку по идентификатору",
    responses={404: {"description": "Заявка не найдена"}},
)
def get_request(request_id: int) -> ServiceRequest:
    item = repository.get(request_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return item


@app.post(
    "/api/v1/routes/",
    response_model=ServiceRequest,
    status_code=status.HTTP_201_CREATED,
    tags=["Service Requests"],
    summary="Создать новую заявку на ТО",
    responses={
        201: {"description": "Заявка создана"},
        400: {"description": "Некорректные входные данные"},
    },
)
def create_request(payload: ServiceRequestCreate) -> ServiceRequest:
    return repository.create(payload)


@app.patch(
    "/api/v1/routes/{request_id}",
    response_model=ServiceRequest,
    status_code=status.HTTP_200_OK,
    tags=["Service Requests"],
    summary="Частично обновить заявку",
    responses={404: {"description": "Заявка не найдена"}},
)
def update_request(request_id: int, patch: ServiceRequestUpdate) -> ServiceRequest:
    updated = repository.update(request_id, patch.model_dump(exclude_none=True))
    if updated is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return updated


@app.delete(
    "/api/v1/routes/{request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Service Requests"],
    summary="Удалить заявку",
    responses={404: {"description": "Заявка не найдена"}},
)
def delete_request(request_id: int) -> JSONResponse:
    if not repository.delete(request_id):
        raise HTTPException(status_code=404, detail="Request not found")
    return JSONResponse(status_code=204, content=None)
