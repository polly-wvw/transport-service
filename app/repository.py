from datetime import datetime
from threading import Lock
from typing import Dict, List, Optional

from app.schemas import RequestStatus, ServiceRequest, ServiceRequestCreate


class InMemoryRepository:
    def __init__(self) -> None:
        self._data: Dict[int, ServiceRequest] = {}
        self._next_id = 1
        self._lock = Lock()

    def list(self) -> List[ServiceRequest]:
        return list(self._data.values())

    def get(self, request_id: int) -> Optional[ServiceRequest]:
        return self._data.get(request_id)

    def create(self, payload: ServiceRequestCreate) -> ServiceRequest:
        with self._lock:
            item = ServiceRequest(
                id=self._next_id,
                status=RequestStatus.NEW,
                created_at=datetime.utcnow(),
                **payload.model_dump(),
            )
            self._data[item.id] = item
            self._next_id += 1
            return item

    def update(self, request_id: int, patch: dict) -> Optional[ServiceRequest]:
        with self._lock:
            item = self._data.get(request_id)
            if item is None:
                return None
            updated = item.model_copy(update=patch)
            self._data[request_id] = updated
            return updated

    def delete(self, request_id: int) -> bool:
        with self._lock:
            return self._data.pop(request_id, None) is not None


repository = InMemoryRepository()
