from typing import Annotated

from fastapi import APIRouter, Depends

from app.appointments.schemas import AppointmentCreateSchema, AppointmentSchema
from app.appointments.service import AppointmentService
from app.dependency import get_appointments_service

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get(
    "/{id}",
    response_model=AppointmentSchema,
)
async def get_appointment_by_id(
        appointment_service: Annotated[
            AppointmentService, Depends(get_appointments_service)
        ],
        appointment_id: int,
):
    appointment = await appointment_service.get_appointment_by_id(appointment_id)
    return appointment


@router.post(
    "/",
    response_model=AppointmentSchema,
)
async def create_appointment(
        body: AppointmentCreateSchema,
        appointment_service: Annotated[
            AppointmentService, Depends(get_appointments_service)
        ],
):
    appointment = await appointment_service.create_appointment(body)
    return appointment
