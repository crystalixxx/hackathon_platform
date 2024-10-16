from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL = ""

# Этот объект отвечает за связь с БД
engine = create_engine(URL)

# Это объект сессии, который будет использоваться для взаимодействия с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  Модели наследуются от этого базового класса
Base = declarative_base()


# Управляет сессиями
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
