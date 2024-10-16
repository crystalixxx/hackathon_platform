from sqlalchemy.orm import Session
import models


# Получает пользователя по ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter_by(id=user_id).first()


# Получает список пользователей
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# Создает нового пользователя
def create_user(db: Session, user: models.User):
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
