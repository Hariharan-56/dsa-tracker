from sqlalchemy import Column, Integer, String, Date, Text
from database import Base


class ProblemEntry(Base):
    __tablename__ = "problem_entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    pattern = Column(String(100))
    difficulty = Column(String(10))
    date_solved = Column(Date, nullable=False)
    time_taken_minutes = Column(Integer)
    status = Column(String(20))
    notes = Column(Text)
    link = Column(String(500))