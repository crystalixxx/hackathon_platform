from fastapi import HTTPException, FastAPI
from pydantic import BaseModel
from typing import List, Type

from services.user_and_teams_service.app.database.models.team import Team
from services.user_and_teams_service.app.database.models.user import User
from . import TeamRepository, UserRepository
from .user import UserRepository
from .team import TeamRepository

app = FastAPI()


@app.get("/users, response_model=List[User]")
def get_users(skip: int = 0, limit: int = 100) -> Type[UserRepository]:
    return UserRepository


@app.get("/teams, response_model=List[Team]")
def get_teams(skip: int = 0, limit: int = 100) -> Type[TeamRepository]:
    return TeamRepository