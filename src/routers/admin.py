from http import HTTPStatus

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

import schemas
from database.admin_crud import AdminCrud
from logger import log

router = APIRouter()


@router.get("/admin/users", response_model=list[schemas.User])
async def get_users(req: Request) -> list[schemas.User] | JSONResponse:
    offset = req.query_params.get("offset")

    if offset and offset.isnumeric():
        offset = int(offset)
    else:
        offset = 0

    try:
        return await AdminCrud().find_users(offset)
    except Exception as error:
        log.error(f"get_users {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content="Cannot get users"
        )
