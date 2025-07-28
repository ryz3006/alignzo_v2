from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from .. import schemas, models, database

router = APIRouter(prefix="/runs", tags=["runs"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.TestRunResponse])
def list_runs(db: Session = Depends(get_db)):
    return db.query(models.TestRun).all()

@router.post("/", response_model=schemas.TestRunResponse)
def create_run(run: schemas.TestRunCreate, db: Session = Depends(get_db)):
    db_run = models.TestRun(**run.dict())
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

@router.get("/{run_id}", response_model=schemas.TestRunResponse)
def get_run(run_id: UUID, db: Session = Depends(get_db)):
    run = db.query(models.TestRun).filter(models.TestRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run 