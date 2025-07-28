from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from .. import schemas, models, database

router = APIRouter(prefix="/artifacts", tags=["artifacts"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.ArtifactResponse])
def list_artifacts(db: Session = Depends(get_db)):
    return db.query(models.Artifact).all()

@router.post("/", response_model=schemas.ArtifactResponse)
def create_artifact(artifact: schemas.ArtifactCreate, db: Session = Depends(get_db)):
    db_artifact = models.Artifact(**artifact.dict())
    db.add(db_artifact)
    db.commit()
    db.refresh(db_artifact)
    return db_artifact

@router.get("/{artifact_id}", response_model=schemas.ArtifactResponse)
def get_artifact(artifact_id: UUID, db: Session = Depends(get_db)):
    artifact = db.query(models.Artifact).filter(models.Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact 