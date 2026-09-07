from pydantic import BaseModel
from datetime import date
from typing import Optional


class ProblemBase(BaseModel):
    title: str
    pattern: Optional[str] = None
    difficulty: Optional[str] = None
    date_solved: date
    time_taken_minutes: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    link: Optional[str] = None


class ProblemCreate(ProblemBase):
    pass


class ProblemOut(ProblemBase):
    id: int

    class Config:
        from_attributes = True