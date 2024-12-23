from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
from enum import Enum
import sqlite3

app = FastAPI()

db_name = "../bank_tickets.db"

def init_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'waiting'
    )
    ''')
    conn.commit()
    conn.close()

init_db()

class Status(Enum):
    WAITING = "waiting"
    PROCESSED = "processed"

class Ticket(BaseModel):
    id: int
    number: int
    date: str
    status: Status

@app.post("/create_ticket/", response_model=Ticket)
def create_ticket():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(number) FROM tickets")
    last_number = cursor.fetchone()[0]
    next_number = (last_number + 1) if last_number else 1

    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO tickets (number, date, status) VALUES (?, ?, ?)",
        (next_number, now, Status.WAITING.value))
    ticket_id = cursor.lastrowid
    conn.commit()

    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=500, detail="Error creating ticket")

    return Ticket(id=row[0], number=row[1], date=row[2], status=Status(row[3]))

@app.get("/tickets/", response_model=List[Ticket])
def get_tickets():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE status = ? ORDER BY number ASC", (Status.WAITING.value,))
    rows = cursor.fetchall()
    conn.close()

    return [Ticket(id=row[0], number=row[1], date=row[2], status=Status(row[3])) for row in rows]

@app.put("/tickets/next/", response_model=Ticket)
def process_next_ticket():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE status = ? ORDER BY number ASC LIMIT 1", (Status.WAITING.value,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="No tickets in the queue")

    ticket_id = row[0]
    cursor.execute("UPDATE tickets SET status = ? WHERE id = ?", (Status.PROCESSED.value, ticket_id))
    conn.commit()
    conn.close()

    return Ticket(id=row[0], number=row[1], date=row[2], status=Status.PROCESSED)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main_5:app", host="127.0.0.1", port=8000, reload=True)

