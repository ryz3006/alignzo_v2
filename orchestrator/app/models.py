from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import uuid
from datetime import datetime

Base = declarative_base()

class TestType(str, enum.Enum):
    functional = "functional"
    load = "load"
    security = "security"

class Test(Base):
    __tablename__ = "tests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    type = Column(Enum(TestType), nullable=False)
    path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TestSuite(Base):
    __tablename__ = "test_suites"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class TestRunStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    passed = "passed"
    failed = "failed"
    cancelled = "cancelled"

class TestRun(Base):
    __tablename__ = "test_runs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    suite_id = Column(UUID(as_uuid=True), ForeignKey('test_suites.id'), nullable=True)
    test_id = Column(UUID(as_uuid=True), ForeignKey('tests.id'), nullable=True)
    status = Column(Enum(TestRunStatus), default=TestRunStatus.pending)
    triggered_by = Column(String)
    environment = Column(String)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    config = Column(JSON)

class TestResultStatus(str, enum.Enum):
    passed = "passed"
    failed = "failed"
    error = "error"
    skipped = "skipped"

class TestResult(Base):
    __tablename__ = "test_results"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey('test_runs.id'))
    test_id = Column(UUID(as_uuid=True), ForeignKey('tests.id'))
    status = Column(Enum(TestResultStatus))
    logs = Column(Text)
    error = Column(Text)
    metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class ArtifactType(str, enum.Enum):
    screenshot = "screenshot"
    video = "video"
    log = "log"
    report = "report"

class Artifact(Base):
    __tablename__ = "artifacts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    result_id = Column(UUID(as_uuid=True), ForeignKey('test_results.id'))
    type = Column(Enum(ArtifactType))
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow) 