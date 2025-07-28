from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database
from ..logging_client import send_audit_log

router = APIRouter(prefix="/appreciations", tags=["appreciations"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.AppreciationResponse])
def list_appreciations(db: Session = Depends(get_db)):
    return db.query(models.Appreciation).all()

@router.post("/", response_model=schemas.AppreciationResponse)
def create_appreciation(appreciation: schemas.AppreciationCreate, db: Session = Depends(get_db)):
    db_appreciation = models.Appreciation(**appreciation.dict())
    db.add(db_appreciation)
    db.commit()
    db.refresh(db_appreciation)
    send_audit_log(db_appreciation.recipient_id, db_appreciation.giver_id, "APPRECIATION_CREATED", {"message": db_appreciation.message})
    return db_appreciation

@router.get("/{appreciation_id}", response_model=schemas.AppreciationResponse)
def get_appreciation(appreciation_id: int, db: Session = Depends(get_db)):
    appreciation = db.query(models.Appreciation).filter(models.Appreciation.appreciation_id == appreciation_id).first()
    if not appreciation:
        raise HTTPException(status_code=404, detail="Appreciation not found")
    return appreciation

@router.put("/{appreciation_id}", response_model=schemas.AppreciationResponse)
def update_appreciation(appreciation_id: int, appreciation_update: schemas.AppreciationCreate, db: Session = Depends(get_db)):
    appreciation = db.query(models.Appreciation).filter(models.Appreciation.appreciation_id == appreciation_id).first()
    if not appreciation:
        raise HTTPException(status_code=404, detail="Appreciation not found")
    for key, value in appreciation_update.dict().items():
        setattr(appreciation, key, value)
    db.commit()
    db.refresh(appreciation)
    send_audit_log(appreciation.recipient_id, appreciation.giver_id, "APPRECIATION_UPDATED", {"message": appreciation.message})
    return appreciation

@router.delete("/{appreciation_id}", status_code=204)
def delete_appreciation(appreciation_id: int, db: Session = Depends(get_db)):
    appreciation = db.query(models.Appreciation).filter(models.Appreciation.appreciation_id == appreciation_id).first()
    if not appreciation:
        raise HTTPException(status_code=404, detail="Appreciation not found")
    send_audit_log(appreciation.recipient_id, appreciation.giver_id, "APPRECIATION_DELETED", {"message": appreciation.message})
    db.delete(appreciation)
    db.commit()
    return 