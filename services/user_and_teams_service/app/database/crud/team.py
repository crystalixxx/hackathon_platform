from sqlalchemy.orm import Session
from app.database.models import Team
from app.database.schemas.team import TeamCreate, TeamUpdate, TeamSchema


def get_teams(db: Session, skip: int = 0, limit: int = 100) -> list[TeamSchema]:
    return db.query(Team).offset(skip).limit(limit).all()


def get_team_by_id(db: Session, team_id: int) -> TeamSchema | None:
    return db.query(Team).filter(Team.id == team_id).first()


def get_team_by_title(db: Session, title: str) -> TeamSchema | None:
    return db.query(Team).filter(Team.title == title).first()


def create_team(db: Session, team: TeamCreate) -> TeamSchema:
    dict_create_team = team.dict(exclude_none=True)
    new_team = Team(**dict_create_team)

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team


def update_team(db: Session, team_id: int, team: TeamUpdate) -> TeamSchema | None:
    old_team = get_team_by_id(db, team_id)

    if old_team is None:
        return None

    dict_update_team = team.dict(exclude_none=True)

    for key, value in dict_update_team.items():
        if value is not None:
            setattr(old_team, key, value)

    db.add(old_team)
    db.commit()
    db.refresh(old_team)

    return old_team


def delete_team(db: Session, team_id: int) -> Team | None:
    team = get_team_by_id(db, team_id)

    if team is None:
        return None

    db.delete(team)
    db.commit()

    return team
