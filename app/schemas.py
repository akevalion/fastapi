from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class Status(str, Enum):
    WAITING = "waiting"
    PROCESSED = "processed"
    CANCELLED = "cancelled"

class Ticket(BaseModel):
    id: int
    number: int
    date: datetime
    status: Status

    model_config = ConfigDict(from_attributes=True)

class TicketUpdate(BaseModel):
    number: Optional[int]
    date: Optional[datetime]
    status: Optional[Status]