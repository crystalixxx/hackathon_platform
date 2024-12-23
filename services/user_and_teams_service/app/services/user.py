from core.security import get_hashed_password, verify_password
from core.utils.unit_of_work import AbstractUnitOfWork
from database.schemas.user import UserCreate, UserUpdate
from database.schemas.user_tag import UserTagCreate, UserTagUpdate
from fastapi import HTTPException
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND


class UserService:
    async def create_user(self, uow: AbstractUnitOfWork, user: UserCreate):
        exists_user = await self.get_user_by_email(uow, user.email)

        if exists_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        user_dict = user.model_dump(exclude_none=True)
        user_dict["hashed_password"] = get_hashed_password(user.password)
        del user_dict["password"]

        async with uow:
            user_id = await uow.users.add_one(user_dict)

            return user_id

    async def sign_up_new_user(self, uow: AbstractUnitOfWork, user: UserCreate):
        existing_user = await self.get_user_by_email(uow, user.email)

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        new_user = await self.create_user(uow, user)
        return new_user

    async def authenticate_user(
        self, uow: AbstractUnitOfWork, email: str, password: str
    ):
        user = await self.get_user_by_email(uow, email)

        if not user:
            return False

        if not verify_password(password, user.hashed_password):
            return False

        return True

    async def get_users(self, uow: AbstractUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users

    async def get_user_by_id(self, uow: AbstractUnitOfWork, user_id: int):
        async with uow:
            user = await uow.users.find_one({"id": user_id})
            return user

    async def get_user_by_email(self, uow: AbstractUnitOfWork, email: str):
        async with uow:
            user = await uow.users.find_one({"email": email})
            return user

    async def update_user(
        self, uow: AbstractUnitOfWork, user: UserUpdate, user_id: int
    ):
        old_user = await self.get_user_by_id(uow, user_id)

        if old_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this id does not exist",
            )

        user_dict = user.model_dump(exclude_unset=True)

        if user_dict.get("password") is not None:
            setattr(
                user_dict, "hashed_password", get_hashed_password(user_dict["password"])
            )
            del user_dict["password"]

        async with uow:
            user = await uow.users.update({"id": user_id}, user_dict)

            return user

    async def delete_user(self, uow: AbstractUnitOfWork, user_id: int):
        user = self.get_user_by_id(uow, user_id)

        if user is None:
            return None

        async with uow:
            user = await uow.users.delete({"id": user_id})

            return user

    async def create_user_tag(self, uow: AbstractUnitOfWork, user_tag: UserTagCreate):
        user_tag_dict = user_tag.model_dump(exclude_none=True)
        existing_tag = await self.get_user_tag_by_name(
            uow, user_tag_dict["user_id"], user_tag_dict["name"]
        )

        if existing_tag is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tag with this name already exists",
            )

        async with uow:
            user_tag = await uow.user_tags.add_one(user_tag_dict)

            return user_tag

    async def get_user_tags(self, uow: AbstractUnitOfWork, user_id: int):
        async with uow:
            user_tags = await uow.user_tags.find_some({"user_id": user_id})

            return user_tags

    async def get_user_tag_by_name(
        self, uow: AbstractUnitOfWork, user_id: int, tag_name: str
    ):
        async with uow:
            user_tag = await uow.user_tags.find_one(
                {"name": tag_name, "user_id": user_id}
            )
            return user_tag

    async def update_user_tag(
        self,
        uow: AbstractUnitOfWork,
        user_tag: UserTagUpdate,
        user_id: int,
        tag_name: str,
    ):
        user_tag_dict = user_tag.model_dump(exclude_none=True)
        old_user_tag = await self.get_user_tag_by_name(uow, user_id, tag_name)

        if old_user_tag is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Tag with this name doesn't found",
            )

        existing_tag = await self.get_user_tag_by_name(
            uow, user_id, user_tag_dict["name"]
        )

        if existing_tag is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tag with this name already exists",
            )

        async with uow:
            user_tag = await uow.user_tags.update(
                {"user_id": user_id, "name": tag_name}, user_tag_dict
            )

            return user_tag

    async def delete_user_tag(
        self, uow: AbstractUnitOfWork, user_id: int, tag_name: str
    ):
        user_tag = self.get_user_tag_by_name(uow, user_id, tag_name)

        if user_tag is None:
            return None

        async with uow:
            user_tag = await uow.user_tags.delete(
                {"user_id": user_id, "name": tag_name}
            )

            return user_tag
