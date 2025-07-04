from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.models import Appointments
from app.appointments.schemas import AppointmentCreateSchema


class AppointmentsRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_appointment(self, appointment: AppointmentCreateSchema) -> int:
        appointment_model = Appointments(
            doctor_id=appointment.doctor_id,
            patient_id=appointment.patient_id,
            start_time=appointment.start_time,
            description=appointment.description,
        )
        async with self.db_session as session:
            session.add(appointment_model)
            await session.commit()
            return appointment_model.id

    async def get_appointment_by_id(self, appointment_id: int) -> Appointments | None:
        query = select(Appointments).where(Appointments.id == appointment_id)
        async with self.db_session as session:
            appointment: Appointments = (
                await session.execute(query)
            ).scalar_one_or_none()
        return appointment
