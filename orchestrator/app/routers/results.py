from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from .. import schemas, models, database

router = APIRouter(prefix="/results", tags=["results"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.TestResultResponse])
def list_results(db: Session = Depends(get_db)):
    return db.query(models.TestResult).all()

@router.post("/", response_model=schemas.TestResultResponse)
def create_result(result: schemas.TestResultCreate, db: Session = Depends(get_db)):
    db_result = models.TestResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

@router.get("/{result_id}", response_model=schemas.TestResultResponse)
def get_result(result_id: UUID, db: Session = Depends(get_db)):
    result = db.query(models.TestResult).filter(models.TestResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result 