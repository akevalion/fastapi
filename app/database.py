from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

db_url = "sqlite:///../bank_tickets.db"
engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)