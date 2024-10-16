from connect_db import engine
from .models import Base

# Инициализация БД

Base.metadata.create_all(bind=engine)
