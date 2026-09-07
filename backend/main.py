from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import engine, Base, get_db
import models
import schemas

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.post("/problems", response_model=schemas.ProblemOut)
def create_problem(problem: schemas.ProblemCreate, db: Session = Depends(get_db)):
    new_entry = models.ProblemEntry(**problem.model_dump())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@app.get("/problems", response_model=list[schemas.ProblemOut])
def list_problems(db: Session = Depends(get_db)):
    return db.query(models.ProblemEntry).all()


@app.get("/problems/{problem_id}", response_model=schemas.ProblemOut)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.ProblemEntry).filter(models.ProblemEntry.id == problem_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Problem not found")
    return entry


@app.put("/problems/{problem_id}", response_model=schemas.ProblemOut)
def update_problem(problem_id: int, updated: schemas.ProblemCreate, db: Session = Depends(get_db)):
    entry = db.query(models.ProblemEntry).filter(models.ProblemEntry.id == problem_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Problem not found")
    for key, value in updated.model_dump().items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry


@app.delete("/problems/{problem_id}")
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.ProblemEntry).filter(models.ProblemEntry.id == problem_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Problem not found")
    db.delete(entry)
    db.commit()
    return {"message": "Deleted successfully"}


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    by_pattern = db.query(models.ProblemEntry.pattern, func.count(models.ProblemEntry.id)).group_by(models.ProblemEntry.pattern).all()
    by_difficulty = db.query(models.ProblemEntry.difficulty, func.count(models.ProblemEntry.id)).group_by(models.ProblemEntry.difficulty).all()
    by_status = db.query(models.ProblemEntry.status, func.count(models.ProblemEntry.id)).group_by(models.ProblemEntry.status).all()

    return {
        "by_pattern": {pattern: count for pattern, count in by_pattern},
        "by_difficulty": {difficulty: count for difficulty, count in by_difficulty},
        "by_status": {status: count for status, count in by_status},
    }