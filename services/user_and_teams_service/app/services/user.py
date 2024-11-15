from app.database.schemas.user import UserCreate, UserUpdate
from app.core.utils.unit_of_work import AbstractUnitOfWork
from app.core.security import get_hashed_password


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

    async def update_user(self, uow: AbstractUnitOfWork, user: UserUpdate, user_id: int):
        old_user = self.get_user_by_id(uow, user_id)

        if old_user is None:
            return None

        user_dict = user.model_dump(exclude_none=True)

        if user_dict["password"] is not None:
            setattr(user_dict, "hashed_password", get_hashed_password(user_dict["password"]))
            del user_dict["password"]

        async with uow:
            user = await uow.users.update({"id": user_id}, user_dict)
            return user

    async def delete_user(self, uow: AbstractUnitOfWork, user_id: int):
        async with uow:
            user = await uow.users.delete({"id": user_id})
            return user
