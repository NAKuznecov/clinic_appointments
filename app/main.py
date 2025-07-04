from fastapi import FastAPI
from app.appointments.handlers import router as appointment_router

app = FastAPI(title='clinic appointments')

app.include_router(appointment_router)

