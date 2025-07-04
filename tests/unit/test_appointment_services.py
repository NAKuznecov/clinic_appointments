import asyncio
from typing import Any
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from pydantic import BaseModel


# Определение моделей данных
class AppointmentCreateSchema(BaseModel):
    doctor_id: int
    patient_id: int
    start_time: datetime
    description: str


class AppointmentSchema(AppointmentCreateSchema):
    id: int


# Интерфейс репозитория
class IAppointmentRepository:
    async def create_appointment(self, body: AppointmentCreateSchema) -> int:
        pass

    async def get_appointment_by_id(self, appointment_id: int) -> dict | None:
        pass


# Контроллер
class AppointmentsController:
    def __init__(self, repo: IAppointmentRepository):
        self.appointment_repository = repo

    async def create_appointment(self, body: AppointmentCreateSchema) -> AppointmentSchema:
        appointment_id = await self.appointment_repository.create_appointment(body)
        appointment = await self.appointment_repository.get_appointment_by_id(appointment_id)

        return AppointmentSchema(**appointment)

    async def get_appointment_by_id(self, appointment_id: int) -> AppointmentSchema:
        appointment = await self.appointment_repository.get_appointment_by_id(appointment_id)
        return AppointmentSchema(**appointment)


# Создание фиктивных объектов для тестирования
@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_repo():
    class MockRepo(IAppointmentRepository):
        async def create_appointment(self, body: AppointmentCreateSchema) -> int:
            return 1  # Возврат фиктивного ID записи

        async def get_appointment_by_id(self, appointment_id: int) -> dict | None:
            if appointment_id == 1:
                return {
                    'id': 1,
                    'doctor_id': 1,
                    'patient_id': 2,
                    'start_time': datetime.fromisoformat('2025-07-08T10:00:00'),
                    'description': 'Test appointment'
                }
            else:
                return None

    return MockRepo()


@pytest.mark.asyncio
async def test_create_appointment(mock_repo):
    controller = AppointmentsController(repo=mock_repo)

    body = AppointmentCreateSchema(
        doctor_id=1,
        patient_id=2,
        start_time=datetime.fromisoformat('2025-07-08T10:00:00'),
        description='Test appointment'
    )

    result = await controller.create_appointment(body)

    assert isinstance(result, AppointmentSchema), "Результат — не экземпляр AppointmentSchema."
    assert result.id == 1, "Полученный ID некорректен."
    assert result.doctor_id == 1, "Неверный doctor_id."
    assert result.patient_id == 2, "Неверный patient_id."
    assert result.start_time.isoformat() == '2025-07-08T10:00:00', "Время назначено неправильно."
    assert result.description == 'Test appointment', "Описания не совпадают."


@pytest.mark.asyncio
async def test_get_appointment_by_id(mock_repo):
    controller = AppointmentsController(repo=mock_repo)

    result = await controller.get_appointment_by_id(1)

    assert isinstance(result, AppointmentSchema), "Возвращённый объект не является объектом типа AppointmentSchema."
    assert result.id == 1, "Полученный ID неправильный."
    assert result.doctor_id == 1, "Неверный doctor_id."
    assert result.patient_id == 2, "Неверный patient_id."
    assert result.start_time.isoformat() == '2025-07-08T10:00:00', "Неправильно установлено время начала встречи."
    assert result.description == 'Test appointment', "Описание назначения неправильное."