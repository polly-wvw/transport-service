from datetime import date, datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class MaintenanceType(str, Enum):
    TO1 = "TO-1"
    TO2 = "TO-2"
    DAILY = "ЕО"
    SEASONAL = "СО"


class RequestStatus(str, Enum):
    NEW = "new"
    VERIFIED = "verified"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


class ServiceRequestBase(BaseModel):
    vehicle_number: str = Field(
        ..., min_length=1, max_length=32,
        description="Инвентарный/бортовой номер единицы подвижного состава",
        examples=["А123ВС77"],
    )
    maintenance_type: MaintenanceType = Field(
        ..., description="Вид технического обслуживания"
    )
    desired_date: date = Field(
        ..., description="Желаемая дата постановки на ТО"
    )
    description: Optional[str] = Field(
        default=None, max_length=1000,
        description="Описание неисправностей/замечаний",
    )


class ServiceRequestCreate(ServiceRequestBase):
    pass


class ServiceRequestUpdate(BaseModel):
    status: Optional[RequestStatus] = None
    desired_date: Optional[date] = None
    description: Optional[str] = None


class ServiceRequest(ServiceRequestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор заявки")
    status: RequestStatus = Field(
        default=RequestStatus.NEW, description="Текущий статус"
    )
    created_at: datetime = Field(..., description="Дата регистрации заявки")
