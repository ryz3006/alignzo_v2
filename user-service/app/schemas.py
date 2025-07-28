from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class CompanyBase(BaseModel):
    company_name: str

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    company_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    job_title: Optional[str] = None
    department: Optional[str] = None
    reporting_manager_id: Optional[UUID] = None

class UserCreate(UserBase):
    company_id: int

class UserResponse(UserBase):
    user_id: UUID
    company_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class EmployeeRatingBase(BaseModel):
    user_id: UUID
    rated_by_id: UUID
    rating_period: datetime
    score: float
    comments: Optional[str] = None

class EmployeeRatingCreate(EmployeeRatingBase):
    pass

class EmployeeRatingResponse(EmployeeRatingBase):
    rating_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class AppreciationBase(BaseModel):
    recipient_id: UUID
    giver_id: UUID
    message: str

class AppreciationCreate(AppreciationBase):
    pass

class AppreciationResponse(AppreciationBase):
    appreciation_id: int
    created_at: datetime
    class Config:
        orm_mode = True 