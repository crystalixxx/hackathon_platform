from sqlalchemy import Column, Integer, String
from .connect_db import Base


# Определяем модель пользователя.
class User(Base):
    __table_name__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
