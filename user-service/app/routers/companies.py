from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database
from ..logging_client import send_audit_log

router = APIRouter(prefix="/companies", tags=["companies"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.CompanyResponse])
def list_companies(db: Session = Depends(get_db)):
    return db.query(models.Company).all()

@router.post("/", response_model=schemas.CompanyResponse)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    send_audit_log(db_company.company_id, None, "COMPANY_CREATED", {"company_name": db_company.company_name})
    return db_company

@router.get("/{company_id}", response_model=schemas.CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.company_id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/{company_id}", response_model=schemas.CompanyResponse)
def update_company(company_id: int, company_update: schemas.CompanyCreate, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.company_id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    for key, value in company_update.dict().items():
        setattr(company, key, value)
    db.commit()
    db.refresh(company)
    send_audit_log(company.company_id, None, "COMPANY_UPDATED", {"company_name": company.company_name})
    return company

@router.delete("/{company_id}", status_code=204)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.company_id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    send_audit_log(company.company_id, None, "COMPANY_DELETED", {"company_name": company.company_name})
    db.delete(company)
    db.commit()
    return 