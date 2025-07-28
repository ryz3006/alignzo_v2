from pydantic import BaseModel, Field
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime

class TestBase(BaseModel):
    name: str
    type: str
    path: Optional[str] = None

class TestCreate(TestBase):
    pass

class TestResponse(TestBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TestSuiteBase(BaseModel):
    name: str
    description: Optional[str] = None

class TestSuiteCreate(TestSuiteBase):
    pass

class TestSuiteResponse(TestSuiteBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class TestRunBase(BaseModel):
    suite_id: Optional[UUID] = None
    test_id: Optional[UUID] = None
    environment: Optional[str] = None
    config: Optional[Any] = None

class TestRunCreate(TestRunBase):
    pass

class TestRunResponse(TestRunBase):
    id: UUID
    status: str
    triggered_by: Optional[str]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]

    class Config:
        orm_mode = True

class TestResultBase(BaseModel):
    run_id: UUID
    test_id: UUID
    status: str
    logs: Optional[str] = None
    error: Optional[str] = None
    metrics: Optional[Any] = None

class TestResultCreate(TestResultBase):
    pass

class TestResultResponse(TestResultBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class ArtifactBase(BaseModel):
    result_id: UUID
    type: str
    url: Optional[str] = None

class ArtifactCreate(ArtifactBase):
    pass

class ArtifactResponse(ArtifactBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True 