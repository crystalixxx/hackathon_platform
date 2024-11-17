from app.core.security import get_hashed_password
from app.core.utils.unit_of_work import AbstractUnitOfWork
from app.database.schemas.user import UserCreate, UserUpdate
from app.database.schemas.user_tag import UserTagCreate, UserTagUpdate


class UserService:
    async def create_user(self, uow: AbstractUnitOfWork, user: UserCreate):
        user_dict = user.model_dump(exclude_none=True)
        user_dict["hashed_password"] = get_hashed_password(user.password)
        del user_dict["password"]

        async with uow:
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

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
        old_user = self.get_user_by_id(uow, user_id)

        if old_user is None:
            return None

        user_dict = user.model_dump(exclude_none=True)

        if user_dict["password"] is not None:
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
        old_user_tag = self.get_user_tag_by_name(uow, user_id, tag_name)

        if old_user_tag is None:
            return None

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
