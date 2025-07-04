from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Appointments(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer)
    patient_id = Column(Integer)
    start_time = Column(DateTime(timezone=True))
    description = Column(String)

    __table_args__ = (
        UniqueConstraint('doctor_id', 'start_time', name='unique_doctor_start_time'),
    )
