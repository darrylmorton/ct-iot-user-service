import logging
from typing import Any
from sqlalchemy import select, insert, column

from . import models, database, config

LOGGER = logging.getLogger(config.SERVICE_NAME)


# TODO limit and skip
async def get_users():
    async with database.async_session() as session:
        async with session.begin():
            stmt = select(models.User).limit(25)
            result = await session.execute(stmt)
            await session.close()

            return result.scalars().all()


async def get_user_by_username(username: str):
    async with database.async_session() as session:
        async with session.begin():
            stmt = select(models.User).where(models.User.username == username)
            result = await session.execute(stmt)
            await session.close()

            return result.scalars().all()


# TODO remove Any
async def post_user(user_request: Any):
    # TODO create pashword_hash and salt
    salt = "salt"

    async with database.async_session() as session:
        user = models.User(
            username=user_request.username,
            password_hash=user_request.password,
            salt=salt,
        )

        async with session.begin():
            session.add(user)
            await session.commit()

        await session.refresh(user)
        await session.close()

        return {"id": user.id, "username": user.username}


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
