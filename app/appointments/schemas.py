from datetime import datetime

from pydantic import BaseModel


class AppointmentCreateSchema(BaseModel):
    doctor_id: int
    patient_id: int
    start_time: datetime
    description: str


class AppointmentSchema(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    start_time: datetime
    description: str
