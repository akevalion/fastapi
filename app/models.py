from datetime import datetime
from app.schemas import Status
from sqlalchemy import Column, Integer, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(SQLAlchemyEnum(Status), nullable=False, default=Status.WAITING)