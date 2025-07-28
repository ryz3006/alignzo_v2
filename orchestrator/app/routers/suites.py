from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from .. import schemas, models, database

router = APIRouter(prefix="/suites", tags=["suites"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.TestSuiteResponse])
def list_suites(db: Session = Depends(get_db)):
    return db.query(models.TestSuite).all()

@router.post("/", response_model=schemas.TestSuiteResponse)
def create_suite(suite: schemas.TestSuiteCreate, db: Session = Depends(get_db)):
    db_suite = models.TestSuite(**suite.dict())
    db.add(db_suite)
    db.commit()
    db.refresh(db_suite)
    return db_suite

@router.get("/{suite_id}", response_model=schemas.TestSuiteResponse)
def get_suite(suite_id: UUID, db: Session = Depends(get_db)):
    suite = db.query(models.TestSuite).filter(models.TestSuite.id == suite_id).first()
    if not suite:
        raise HTTPException(status_code=404, detail="Suite not found")
    return suite 