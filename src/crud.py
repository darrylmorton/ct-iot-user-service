import logging
import bcrypt

from sqlalchemy import select
from starlette.responses import JSONResponse

from .config import SERVICE_NAME
from .schemas import User
from .database import async_session
from .models import UserModel

LOGGER = logging.getLogger(SERVICE_NAME)


async def find_users(offset=0) -> list[User]:
    async with async_session() as session:
        async with session.begin():
            stmt = select(UserModel).limit(25).offset(offset)
            result = await session.execute(stmt)
            await session.close()

            return result.scalars().all()


async def find_user_by_username(username: str) -> User:
    async with async_session() as session:
        async with session.begin():
            stmt = select(UserModel).where(UserModel.username == username)
            result = await session.execute(stmt)
            await session.close()

            return result.scalars().first()


async def add_user(_username: str, _password: str) -> JSONResponse | User:
    password = _password.encode("utf-8")

    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password, salt).decode(encoding="utf-8")

    async with async_session() as session:
        user = UserModel(username=_username, password_hash=password_hash)

        async with session.begin():
            session.add(user)
            await session.commit()

        await session.refresh(user)
        await session.close()

        return User(id=user.id, username=user.username)


# async def get_user_details(db: AsyncSession):
#     async with database.async_session() as db:
#         async with db.begin():
#             stmt = select(
#                 models.UserDetails.id,
#                 models.UserDetails.user_id,
#                 models.UserDetails.first_name,
#                 models.UserDetails.last_name,
#             )
#
#             result = await db.execute(stmt)
#
#             await db.close()
#
#             return result
