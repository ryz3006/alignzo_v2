from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from .. import schemas, models, database

router = APIRouter(prefix="/tests", tags=["tests"])

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.TestResponse])
def list_tests(db: Session = Depends(get_db)):
    return db.query(models.Test).all()

@router.post("/", response_model=schemas.TestResponse)
def create_test(test: schemas.TestCreate, db: Session = Depends(get_db)):
    db_test = models.Test(**test.dict())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

@router.get("/{test_id}", response_model=schemas.TestResponse)
def get_test(test_id: UUID, db: Session = Depends(get_db)):
    test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test 