import asyncio
from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy import Column, DateTime, Integer, String, select
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.schema import CreateTable

from app.appointments.models import Appointments
from app.database.database import Base
from app.settings import Settings


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer)
    patient_id = Column(Integer)
    start_time = Column(DateTime)
    description = Column(String)


@pytest.fixture
def settings():
    return Settings()


engine = create_async_engine(
    url="sqlite+aiosqlite:///test.db", future=True, echo=True, pool_pre_ping=True
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(autouse=True, scope="function")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def get_db_session() -> AsyncSession:
    yield AsyncSessionFactory()


pytestmark = pytest.mark.asyncio


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(CreateTable(Appointments.__table_args__), checkfirst=True)


async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all, checkfirst=True)


async def test_create_and_get_appointment(get_db_session):
    appointment_model = Appointments(
        id=1,
        doctor_id=1,
        patient_id=2,
        start_time=datetime.fromisoformat("2025-12-03T10:00:00"),
        description="some",
    )
    async with get_db_session() as session:
        session.add(appointment_model)
        await session.commit()
        assert isinstance(appointment_model, Appointments)

        # Немедленно считываем назначение
        appointment = (
            await session.execute(select(Appointments).where(Appointments.id == 1))
        ).scalar_one_or_none()
        assert appointment is not None
        assert appointment.doctor_id == 1


if __name__ == "__main__":
    asyncio.run(create_tables())
    test_create_and_get_appointment(get_db_session)
    asyncio.run(drop_all_tables())
