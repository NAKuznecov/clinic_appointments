import dataclasses

from app.appointments.repository import AppointmentsRepository
from app.appointments.schemas import AppointmentSchema, AppointmentCreateSchema


@dataclasses.dataclass
class AppointmentService:
    def __init__(self, appointment_repository: AppointmentsRepository):
        self.appointment_repository = appointment_repository

    async def create_appointment(self, body: AppointmentCreateSchema) -> AppointmentSchema:
        appointment_id = await self.appointment_repository.create_appointment(body)
        appointment_schema = await self.get_appointment_by_id(appointment_id)
        return AppointmentSchema.model_validate(appointment_schema)

    async def get_appointment_by_id(self, appointment_id) -> AppointmentSchema:
        appointment = await self.appointment_repository.get_appointment_by_id(appointment_id)
        appointment_schema = AppointmentSchema(
            id=appointment.id,
            doctor_id=appointment.doctor_id,
            patient_id=appointment.patient_id,
            start_time=appointment.start_time,
            description=appointment.description,
        )
        return AppointmentSchema.model_validate(appointment_schema)
