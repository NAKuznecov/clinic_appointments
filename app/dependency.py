from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.appointments.repository import AppointmentsRepository
from app.appointments.service import AppointmentService
from app.database.accessor import get_db_session


async def get_appointments_repository(db_session: AsyncSession = Depends(get_db_session)) -> AppointmentsRepository:
    return AppointmentsRepository(db_session)


async def get_appointments_service(
        appointment_repository: AppointmentsRepository = Depends(get_appointments_repository),
) -> AppointmentService:
    return AppointmentService(appointment_repository=appointment_repository)
