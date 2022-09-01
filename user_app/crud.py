import hashlib
from typing import List
from uuid import NAMESPACE_X500, uuid5

from sqlalchemy import and_, update
from sqlalchemy.future import select

from quiz_project.behaviours.base_manager import AbstractBaseManager
from .models import User
from .schemas import UserCreate


class UserManager(AbstractBaseManager):
    async def check_user_credentials(self, username: str, password: str):
        salt = uuid5(NAMESPACE_X500, username).hex.encode()
        hashed_password = hashlib.sha512(password.encode() + salt).hexdigest()
        query = select(User).where(
            and_(User.username == username,
                 User.hashed_password == hashed_password)
        )
        response = await self._database_session.execute(query)
        return response.scalars().first()

    async def get_user(self, user_id: int):
        query = select(User).where(User.id == user_id)
        response = await self._database_session.execute(query)
        return response.scalars().first()

    async def get_user_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        response = await self._database_session.execute(query)
        return response.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        response = await self._database_session.execute(query)
        return response.scalars().first()

    async def get_users(self):
        query = select(User)
        response = await self._database_session.execute(query)
        return response.scalars().all()

    async def hash_password(self, user: UserCreate, password: str):
        salt = uuid5(NAMESPACE_X500, user.username).hex.encode()
        return hashlib.sha512(password.encode() + salt).hexdigest()

    async def create_user(self, user: UserCreate):
        password = await self.hash_password(user, user.password)
        db_user = User(
            username=user.username, hashed_password=password, email=user.email
        )
        await self.create(db_user)

        return db_user

    async def update_user_password(self, user: User, new_password: str):
        hashed_password = await self.hash_password(user, new_password)
        query = update(User).where(User.id == user.id).values(hashed_password=hashed_password)
        await self._database_session.execute(query)

    async def create_moderators(self, user_ids: List[int], value: bool):
        query = update(User).where(User.id.in_(user_ids)).values(is_moderator=value)
        await self._database_session.execute(query)
