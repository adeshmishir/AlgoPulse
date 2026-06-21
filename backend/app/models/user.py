
from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    ranking = Column(Integer)

    total_solved = Column(Integer)

    easy = Column(Integer)

    medium = Column(Integer)

    hard = Column(Integer)

    acceptance = Column(Float)