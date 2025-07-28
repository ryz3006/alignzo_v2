from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database
from ..logging_client import send_audit_log

router = APIRouter(prefix="/ratings", tags=["ratings"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.EmployeeRatingResponse])
def list_ratings(db: Session = Depends(get_db)):
    return db.query(models.EmployeeRating).all()

@router.post("/", response_model=schemas.EmployeeRatingResponse)
def create_rating(rating: schemas.EmployeeRatingCreate, db: Session = Depends(get_db)):
    db_rating = models.EmployeeRating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    send_audit_log(db_rating.user_id, db_rating.rated_by_id, "RATING_CREATED", {"score": float(db_rating.score)})
    return db_rating

@router.get("/{rating_id}", response_model=schemas.EmployeeRatingResponse)
def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(models.EmployeeRating).filter(models.EmployeeRating.rating_id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

@router.put("/{rating_id}", response_model=schemas.EmployeeRatingResponse)
def update_rating(rating_id: int, rating_update: schemas.EmployeeRatingCreate, db: Session = Depends(get_db)):
    rating = db.query(models.EmployeeRating).filter(models.EmployeeRating.rating_id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    for key, value in rating_update.dict().items():
        setattr(rating, key, value)
    db.commit()
    db.refresh(rating)
    send_audit_log(rating.user_id, rating.rated_by_id, "RATING_UPDATED", {"score": float(rating.score)})
    return rating

@router.delete("/{rating_id}", status_code=204)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(models.EmployeeRating).filter(models.EmployeeRating.rating_id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    send_audit_log(rating.user_id, rating.rated_by_id, "RATING_DELETED", {"score": float(rating.score)})
    db.delete(rating)
    db.commit()
    return 