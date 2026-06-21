from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class ProfileHistory(Base):
    __tablename__ = "profile_history"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, nullable=False)

    ranking = Column(Integer)

    total_solved = Column(Integer)

    easy = Column(Integer)

    medium = Column(Integer)

    hard = Column(Integer)

    acceptance = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)