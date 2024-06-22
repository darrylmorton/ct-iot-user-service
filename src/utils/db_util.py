from sqlalchemy import select

import models


def find_users_stmt(offset=0):
    return select(models.UserModel).limit(25).offset(offset)


def find_user_by_username_stmt(username: str):
    return select(models.UserModel).where(username == models.UserModel.username)


def add_user_model(username: str, password_hash: str):
    return models.UserModel(username=username, password_hash=password_hash)
