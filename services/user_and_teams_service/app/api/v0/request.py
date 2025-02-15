from app.api.dependencies import UOWAlchemyDep
from app.core.auth import get_current_user
from app.database.schemas.request import RequestCreate, RequestSchema
from app.services.request import RequestService
from app.services.team import TeamService
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

request_router = APIRouter()


@request_router.get("/user/{user_id}", response_model=list[RequestSchema])
async def get_requests_from_user(
    uow: UOWAlchemyDep, user_id: int, current_user=Depends(get_current_user)
):
    if current_user.role not in ["user"] and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are not authorized to access this resource",
        )

    return await RequestService().get_requests_of_user(uow, user_id)


@request_router.get("/by_team/{team_id}", response_model=list[RequestSchema])
async def get_requests_from_team(
    uow: UOWAlchemyDep, team_id: int, current_user=Depends(get_current_user)
):
    if not TeamService().is_member_of_team(uow, team_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are not authorized to access this resource",
        )

    return await RequestService().get_requests_sent_by_team(uow, team_id)


@request_router.get("/to_team/{team_id}", response_model=list[RequestSchema])
async def get_requests_to_team(
    uow: UOWAlchemyDep, team_id: int, current_user=Depends(get_current_user)
):
    if not TeamService().is_member_of_team(uow, team_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are not authorized to access this resource",
        )

    return await RequestService().get_requests_to_team(uow, team_id)


@request_router.post("/")
async def create_request(
    uow: UOWAlchemyDep, request: RequestCreate, current_user=Depends(get_current_user)
):
    if current_user.role not in ["user"] and current_user.id != request.user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are not authorized to access this resource",
        )

    return await RequestService().create_request(uow, request)


@request_router.patch("/approve/{request_id}", response_model=RequestSchema)
async def approve_request(
    uow: UOWAlchemyDep, request_id: int, current_user=Depends(get_current_user)
):
    request = await RequestService().get_request_by_id(uow, request_id)
    team = await TeamService().get_team_by_id(uow, request.request_team_id)

    if current_user.role not in ["user"]:
        if (
            request.send_by_team
            and team.captain_id != current_user.id
            or not request.send_by_team
            and request.user_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You are not authorized to access this resource",
            )

    return await RequestService().approve_request(uow, request_id)


@request_router.patch("/reject/{request_id}", response_model=RequestSchema)
async def reject_request(
    uow: UOWAlchemyDep, request_id: int, current_user=Depends(get_current_user)
):
    request = await RequestService().get_request_by_id(uow, request_id)
    team = await TeamService().get_team_by_id(uow, request.request_team_id)

    if current_user.role not in ["user"]:
        if (
            request.send_by_team
            and team.captain_id != current_user.id
            or not request.send_by_team
            and request.user_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You are not authorized to access this resource",
            )

    return await RequestService().reject_request(uow, request_id)


@request_router.delete("/{request_id}", response_model=RequestSchema)
async def delete_request(
    uow: UOWAlchemyDep, request_id: int, current_user=Depends(get_current_user)
):
    request = await RequestService().get_request_by_id(uow, request_id)
    team = await TeamService().get_team_by_id(uow, request.request_team_id)

    if current_user.role not in ["user"]:
        if (
            request.sent_by_team
            and current_user.id != team.captain_id
            or not request.send_by_team
            and current_user != request.user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You are not authorized to access this resource",
            )

    return await RequestService().delete_request(uow, request_id)
