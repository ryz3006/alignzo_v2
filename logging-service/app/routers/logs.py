from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from .. import models, database
from ..logging_utils import setup_logger, archive_and_purge_logs

router = APIRouter(prefix="/logs", tags=["logs"])
logger = setup_logger()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=201)
def ingest_log(
    company_id: int,
    user_id: Optional[str] = None,
    action: str = Query(...),
    details: Optional[dict] = None,
    db: Session = Depends(get_db)
):
    log_entry = models.AuditLog(
        company_id=company_id,
        user_id=user_id,
        action=action,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.add(log_entry)
    db.commit()
    logger.info(f"{log_entry.timestamp} | company_id={company_id} | user_id={user_id} | action={action} | details={details}")
    archive_and_purge_logs()
    return {"status": "logged"}

@router.get("/", response_model=List[dict])
def search_logs(
    company_id: Optional[int] = None,
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.AuditLog)
    if company_id:
        query = query.filter(models.AuditLog.company_id == company_id)
    if user_id:
        query = query.filter(models.AuditLog.user_id == user_id)
    if action:
        query = query.filter(models.AuditLog.action == action)
    if start_time:
        query = query.filter(models.AuditLog.timestamp >= start_time)
    if end_time:
        query = query.filter(models.AuditLog.timestamp <= end_time)
    results = query.order_by(models.AuditLog.timestamp.desc()).all()
    return [
        {
            "log_id": log.log_id,
            "company_id": log.company_id,
            "user_id": str(log.user_id) if log.user_id else None,
            "action": log.action,
            "details": log.details,
            "timestamp": log.timestamp.isoformat()
        }
        for log in results
    ] 