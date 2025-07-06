from sqlalchemy import Column, String, Boolean, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class Musician(Base):
    __tablename__ = "musicians"
    id = Column(String, primary_key=True)
    hostname = Column(String)
    ip = Column(String)
    last_seen = Column(DateTime, default=datetime.datetime.utcnow)
    locked = Column(Boolean, default=False)
    current_task = Column(String, nullable=True)
    avg_latency = Column(Float, nullable=True)
    offline = Column(Boolean, default=False)

engine = create_engine("sqlite:///orchestrator.db", echo=False)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()