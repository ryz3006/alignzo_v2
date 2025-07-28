from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, DECIMAL, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    company_id = Column(Integer, primary_key=True)
    company_name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    users = relationship('User', back_populates='company')

class User(Base):
    __tablename__ = 'users'
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(Integer, ForeignKey('companies.company_id', ondelete='CASCADE'), nullable=False)
    email = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    job_title = Column(String)
    department = Column(String)
    reporting_manager_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    company = relationship('Company', back_populates='users')
    ratings = relationship('EmployeeRating', back_populates='user', foreign_keys='EmployeeRating.user_id')
    given_ratings = relationship('EmployeeRating', back_populates='rated_by', foreign_keys='EmployeeRating.rated_by_id')
    appreciations_received = relationship('Appreciation', back_populates='recipient', foreign_keys='Appreciation.recipient_id')
    appreciations_given = relationship('Appreciation', back_populates='giver', foreign_keys='Appreciation.giver_id')
    __table_args__ = (UniqueConstraint('company_id', 'email', name='uq_company_email'),)

class EmployeeRating(Base):
    __tablename__ = 'employee_ratings'
    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    rated_by_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    rating_period = Column(DateTime, nullable=False)
    score = Column(DECIMAL(3, 2), nullable=False)
    comments = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user = relationship('User', back_populates='ratings', foreign_keys=[user_id])
    rated_by = relationship('User', back_populates='given_ratings', foreign_keys=[rated_by_id])

class Appreciation(Base):
    __tablename__ = 'appreciations'
    appreciation_id = Column(Integer, primary_key=True, autoincrement=True)
    recipient_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    giver_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    recipient = relationship('User', back_populates='appreciations_received', foreign_keys=[recipient_id])
    giver = relationship('User', back_populates='appreciations_given', foreign_keys=[giver_id]) 