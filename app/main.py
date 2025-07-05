from fastapi import FastAPI

from app.appointments.handlers import router as appointment_router
from app.appointments.models import Base
from app.database.accessor import engine

app = FastAPI(title="clinic appointments")

app.include_router(appointment_router)


if __name__ == "__main__":
    Base.metadata.create_all(engine)