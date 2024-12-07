from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_409_CONFLICT

from app.api.dependencies import UOWAlchemyDep
from app.core.auth import get_current_user
from app.database.schemas.team import TeamCreate, TeamSchema, TeamUpdate, TeamUserSchema
from app.database.schemas.user_tag import UserTagSchema
from app.services.team import TeamService

team_router = APIRouter()


@team_router.get("/", response_model=list[TeamSchema])
async def get_all_teams(uow: UOWAlchemyDep):
    return await TeamService().get_teams(uow)


@team_router.get("/id/{team_id}", response_model=TeamSchema)
async def get_team_by_id(team_id: int, uow: UOWAlchemyDep):
    return await TeamService().get_team_by_id(uow, team_id)


@team_router.get("/captain_id/{captain_id}", response_model=list[TeamSchema])
async def get_teams_by_captain_id(uow: UOWAlchemyDep, captain_id: int):
    return await TeamService().get_teams_by_captain_id(uow, captain_id)


@team_router.get("/name/{team_name}", response_model=TeamSchema)
async def get_team_by_name(uow: UOWAlchemyDep, team_name: str):
    return await TeamService().get_team_by_name(uow, team_name)


@team_router.get("/is_member/{team_id}/{user_id}")
async def get_is_member(uow: UOWAlchemyDep, team_id: int, user_id: int):
    return await TeamService().is_member_of_team(uow, team_id, user_id)


@team_router.get("/members/{team_id}", response_model=list[TeamUserSchema])
async def get_members_of_team(uow: UOWAlchemyDep, team_id: int):
    return await TeamService().get_team_members(uow, team_id)


@team_router.get("/tag/{team_id}", response_model=list[UserTagSchema])
async def get_tags_of_team(uow: UOWAlchemyDep, team_id: int):
    return await TeamService().get_team_tags(uow, team_id)


@team_router.post("/")
async def create_new_team(
    uow: UOWAlchemyDep, team: TeamCreate, current_user=Depends(get_current_user)
):
    if current_user.role not in ["user"] and team.captain_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="You are not allowed to create the team",
        )

    return await TeamService().create_team(uow, team)


@team_router.post("/member/{team_id}/{user_id}")
async def add_member_to_team(
    uow: UOWAlchemyDep,
    team_id: int,
    user_id: int,
    current_user=Depends(get_current_user),
):
    team = await TeamService().get_team_by_id(uow, team_id)

    if current_user.role not in ["user"] and team.captain_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="You are not allowed to add members to the team",
        )

    return await TeamService().add_member(uow, team_id, user_id)


@team_router.patch("/{team_id}", response_model=TeamSchema)
async def update_team(
    uow: UOWAlchemyDep,
    team: TeamUpdate,
    team_id: int,
    current_user=Depends(get_current_user),
):
    if current_user.role not in ["user"] and team.captain_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="You are not allowed to update the team",
        )

    return await TeamService().update_team(uow, team, team_id)


@team_router.delete("/{team_id}", response_model=TeamSchema)
async def delete_team(
    uow: UOWAlchemyDep, team_id: int, current_user=Depends(get_current_user)
):
    team = await TeamService().get_team_by_id(uow, team_id)

    if current_user.role not in ["user"] and team.captain_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="You are not allowed to delete the team",
        )

    return await TeamService().delete_team(uow, team_id)


@team_router.delete("/member/{team_id}/{user_id}")
async def remove_member_from_team(
    uow: UOWAlchemyDep,
    team_id: int,
    user_id: int,
    current_user=Depends(get_current_user),
):
    team = await TeamService().get_team_by_id(uow, team_id)

    if current_user.role not in ["user"] and team.captain_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="You are not allowed to remove members from the team",
        )

    return await TeamService().remove_member(uow, team_id, user_id)
