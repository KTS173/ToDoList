import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Time
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import date, datetime, timezone, time
from typing import Optional
from pydantic import BaseModel


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app_user:app_pass@db:5432/app_dev")

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    email    = Column(String,  unique=True, index=True)
    password = Column(String)
    name     = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)

    tasks       = relationship("TaskDB", back_populates="user",  foreign_keys="TaskDB.user_id")
    projects    = relationship("ProjectDB",       back_populates="owner")
    memberships = relationship("ProjectMemberDB", back_populates="user")


class TaskAssigneeDB(Base):
    __tablename__ = "task_assignees"
    id      = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

class TaskDB(Base):
    __tablename__ = "tasks"

    id           = Column(Integer,      primary_key=True, index=True)
    title        = Column(String(200),  nullable=False)
    is_completed = Column(Boolean,      default=False)
    due_date     = Column(Date,         nullable=True)
    due_time     = Column(Time,         nullable=True)
    created_at   = Column(DateTime,     default=lambda: datetime.now(timezone.utc))
    status       = Column(String(50),   default="Not started")
    description  = Column(String(1000), nullable=True)
    project_id   = Column(Integer,      ForeignKey("projects.id"), nullable=True)
    project_type = Column(String(50),   nullable=True)
    user_id      = Column(Integer,      ForeignKey("users.id"),    nullable=True)


    project  = relationship("ProjectDB", back_populates="tasks")
    user     = relationship("User", back_populates="tasks",    foreign_keys=[user_id])


class ProjectDB(Base):
    __tablename__ = "projects"

    id          = Column(Integer,     primary_key=True, index=True)
    name        = Column(String(200), nullable=False)
    emoji       = Column(String(10),  default="💡")
    type        = Column(String(50),  nullable=False)
    created_at  = Column(DateTime,    default=lambda: datetime.now(timezone.utc))
    color       = Column(String(20),  default="#3b82f6")
    description = Column(String(500), nullable=True)
    user_id     = Column(Integer,     ForeignKey("users.id"), nullable=True)  # ✅ owner

    tasks   = relationship("TaskDB",         back_populates="project", cascade="all, delete-orphan")
    members = relationship("ProjectMemberDB", back_populates="project", cascade="all, delete-orphan") 
    owner   = relationship("User",           back_populates="projects", foreign_keys=[user_id])


class ProjectMemberDB(Base):
    __tablename__ = "project_members"

    id         = Column(Integer,    primary_key=True, index=True)
    project_id = Column(Integer,    ForeignKey("projects.id"), nullable=False)
    user_id    = Column(Integer,    ForeignKey("users.id"),    nullable=False)
    role       = Column(String(50), default="Member")
    added_at   = Column(DateTime,   default=lambda: datetime.now(timezone.utc))

    project = relationship("ProjectDB", back_populates="members")
    user    = relationship("User",      back_populates="memberships")


# ── Pydantic Models ──

class Task(BaseModel):
    id:           Optional[int]      = None
    title:        Optional[str]      = None
    is_completed: Optional[bool]     = None
    due_date:     Optional[date]     = None
    created_at:   Optional[datetime] = None
    status:       Optional[str]      = None
    description:  Optional[str]      = None
    project_id:   Optional[int]      = None
    due_time:     Optional[time]     = None
    project_type: Optional[str]      = None
    user_id:      Optional[int]      = None
    assignee_ids: Optional[list[int]] = None

    model_config = {"from_attributes": True}


class Project(BaseModel):
    id:          Optional[int]      = None
    name:        Optional[str]      = None
    emoji:       Optional[str]      = None
    type:        Optional[str]      = None
    created_at:  Optional[datetime] = None
    color:       Optional[str]      = None
    description: Optional[str]      = None
    user_id:     Optional[int]      = None

    model_config = {"from_attributes": True}


class ProjectMember(BaseModel):
    user_id: Optional[int] = None
    role:    Optional[str] = None
    email:   Optional[str] = None
    name:    Optional[str] = None
    avatar_url: Optional[str] = None 

    model_config = {"from_attributes": True}