from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from datetime import datetime, timezone
from typing import List
from app.database import SessionLocal, init_db
from app.models import TicketModel, Status
from app.schemas import Ticket
from sqlalchemy.orm import Session

app = FastAPI()

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/")
def read_root():
    return {"message": "Server is running"}

@app.post("/create_ticket/", response_model=Ticket)
def create_ticket(session: Session = Depends(get_db)):
    try:
        last_ticket = session.query(TicketModel).order_by(TicketModel.number.desc()).first()
        next_number = (last_ticket.number + 1) if last_ticket else 1

        now = datetime.now(timezone.utc)
        new_ticket = TicketModel(number=next_number, date=now, status=Status.WAITING)
        session.add(new_ticket)
        session.commit()
        session.refresh(new_ticket)

        return Ticket.model_validate(new_ticket)
    finally:
        session.close()

@app.get("/tickets/", response_model=List[Ticket])
def get_tickets(session: Session = Depends(get_db)):
    try:
        tickets = (session.query(TicketModel)
                   .filter_by(status=Status.WAITING)
                   .order_by(TicketModel.number).all())
        return [Ticket.model_validate(ticket) for ticket in tickets]
    finally:
        session.close()

@app.put("/next_ticket/", response_model=Ticket)
def process_next_ticket(session: Session = Depends(get_db)):
    try:
        next_ticket = session.query(TicketModel).filter_by(status=Status.WAITING).order_by(TicketModel.number).first()
        if not next_ticket:
            raise HTTPException(status_code=404, detail="No tickets in the queue")

        next_ticket.status = Status.PROCESSED
        session.commit()
        session.refresh(next_ticket)

        return Ticket.model_validate(next_ticket)
    finally:
        session.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
