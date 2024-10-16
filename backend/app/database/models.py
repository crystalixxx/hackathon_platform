from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()


# Базовая модель
class BaseModel(Base):
    __abstract__ = True  # Указывает, что это абстрактный класс
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


# Модель для таблицы 'user'
class User(BaseModel):
    __table_name__ = "user"

    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    second_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    tags = relationship("UserTag", back_populates="user", lazy="joined")
    hackathons = relationship(
        "OrganizerHackathon", back_populates="user", lazy="joined"
    )


# Модель для связи 'user_tag'
class UserTag(Base):
    __table_name__ = "user_tag"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)

    user = relationship("User", back_populates="tags")
    tag = relationship("Tag", back_populates="users")


# Модель для 'tag'
class Tag(BaseModel):
    __table_name__ = "tag"

    title = Column(String, nullable=False)
    color = Column(String)

    users = relationship("UserTag", back_populates="tag", lazy="joined")
    tasks = relationship("TaskTag", back_populates="tag", lazy="joined")


# Модель для 'hackathon'
class Hackathon(BaseModel):
    __table_name__ = "hackathon"

    title = Column(String, nullable=False)
    description = Column(Text)
    prize = Column(Text)
    status_id = Column(Integer, ForeignKey("hackathon_status.id"))
    redirect_link = Column(String)
    poster_link = Column(String)

    tasks = relationship("HackathonTask", back_populates="hackathon", lazy="joined")
    tags = relationship("HackathonTag", back_populates="hackathon", lazy="joined")
    organizers = relationship(
        "OrganizerHackathon", back_populates="hackathon", lazy="joined"
    )
    status = relationship("HackathonStatus", back_populates="hackathons", lazy="joined")


# Модель для связи 'hackathon_task'
class HackathonTask(Base):
    __table_name__ = "hackathon_task"

    hackathon_id = Column(Integer, ForeignKey("hackathon.id"), primary_key=True)
    task_id = Column(Integer, ForeignKey("task.id"), primary_key=True)

    hackathon = relationship("Hackathon", back_populates="tasks")
    task = relationship("Task", back_populates="hackathons")


# Модель для задачи 'task'
class Task(BaseModel):
    __table_name__ = "task"

    title = Column(String, nullable=False)
    description = Column(Text)

    hackathons = relationship("HackathonTask", back_populates="task", lazy="joined")
    tags = relationship("TaskTag", back_populates="task", lazy="joined")


# Модель для связи 'task_tag'
class TaskTag(Base):
    __table_name__ = "task_tag"

    task_id = Column(Integer, ForeignKey("task.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)

    task = relationship("Task", back_populates="tags")
    tag = relationship("Tag", back_populates="tasks")


# Модель для связи 'organizer_hackathon'
class OrganizerHackathon(Base):
    __table_name__ = "organizer_hackathon"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    hackathon_id = Column(Integer, ForeignKey("hackathon.id"), primary_key=True)

    user = relationship("User", back_populates="hackathons")
    hackathon = relationship("Hackathon", back_populates="organizers")


# Модель для 'hackathon_type'
class HackathonType(BaseModel):
    __table_name__ = "hackathon_type"

    title = Column(String, nullable=False)

    hackathons = relationship("HackathonTypeLink", back_populates="type", lazy="joined")


# Модель для связи 'hackathon_type_link'
class HackathonTypeLink(Base):
    __table_name__ = "hackathon_type_link"

    hackathon_id = Column(Integer, ForeignKey("hackathon.id"), primary_key=True)
    type_id = Column(Integer, ForeignKey("hackathon_type.id"), primary_key=True)

    hackathon = relationship("Hackathon", back_populates="types")
    type = relationship("HackathonType", back_populates="hackathons")


# Модель для 'hackathon_location'
class HackathonLocation(BaseModel):
    __table_name__ = "hackathon_location"

    title = Column(String, nullable=False)

    hackathons = relationship(
        "HackathonLocationLink", back_populates="location", lazy="joined"
    )


# Модель для связи 'hackathon_location_link'
class HackathonLocationLink(Base):
    __table_name__ = "hackathon_location_link"

    hackathon_id = Column(Integer, ForeignKey("hackathon.id"), primary_key=True)
    location_id = Column(Integer, ForeignKey("hackathon_location.id"), primary_key=True)

    hackathon = relationship("Hackathon", back_populates="locations")
    location = relationship("HackathonLocation", back_populates="hackathons")


# Модель для 'hackathon_status'
class HackathonStatus(BaseModel):
    __table_name__ = "hackathon_status"

    title = Column(String, nullable=False)

    hackathons = relationship("Hackathon", back_populates="status", lazy="joined")


# Модель для связи 'hackathon_tag'
class HackathonTag(Base):
    __table_name__ = "hackathon_tag"

    hackathon_id = Column(Integer, ForeignKey("hackathon.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)

    hackathon = relationship("Hackathon", back_populates="tags")
    tag = relationship("Tag", back_populates="hackathons")
