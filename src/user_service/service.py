import contextlib
from http import HTTPStatus
from uuid import UUID

import requests

import sentry_sdk
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from starlette.requests import Request
from starlette.responses import JSONResponse

import config
import crud
from logger import log
from config import SERVICE_NAME, JWT_EXCLUDED_ENDPOINTS
from routers import health, users, user_details, signup, login
from utils import app_util

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme.auto_error = False


async def run_migrations():
    log.info("Running migrations...")

    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

        log.info("Migrations completed successfully")
    except Exception as error:
        log.error(f"Database migration error on startup: {error}")


@contextlib.asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    log.info(f"Starting {SERVICE_NAME}...{app.host}")

    if config.ENVIRONMENT == "production":
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for tracing.
            traces_sample_rate=config.SENTRY_TRACES_SAMPLE_RATE,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=config.SENTRY_PROFILES_SAMPLE_RATE,
            sample_rate=config.SENTRY_SAMPLE_RATE,
            environment=config.ENVIRONMENT,
            server_name=config.SERVICE_NAME,
            integrations=[
                StarletteIntegration(
                    transaction_style="endpoint",
                    failed_request_status_codes=[403, range(500, 599)],
                ),
                FastApiIntegration(
                    transaction_style="endpoint",
                    failed_request_status_codes=[403, range(500, 599)],
                ),
            ],
        )

    await run_migrations()

    log.info(f"{SERVICE_NAME} is ready")

    yield
    log.info(f"{SERVICE_NAME} is shutting down...")


app = FastAPI(title="FastAPI server", lifespan=lifespan_wrapper)


@app.middleware("http")
async def authenticate(request: Request, call_next):
    request_path = request["path"]

    if request_path not in JWT_EXCLUDED_ENDPOINTS:
        auth_token = request.headers["Authorization"]

        if not auth_token:
            log.debug("authenticate - missing auth token")

            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
            )

        response = requests.get(
            f"{config.AUTH_SERVICE_URL}/jwt", headers={"Authorization": auth_token}
        )

        if response.status_code != HTTPStatus.OK:
            log.debug("authenticate - invalid token")

            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
            )

        response_json = response.json()

        _id = response_json["id"]

        if not app_util.validate_uuid4(_id):
            log.debug("authenticate - invalid uuid")

            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
            )

        user = await crud.find_user_by_id_and_enabled(_id=_id)

        if not user or user.id != UUID(_id):
            log.debug("authenticate - user not found")

            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
            )

    return await call_next(request)


app.include_router(health.router, include_in_schema=False)

app.include_router(signup.router, prefix="/api", tags=["signup"])
app.include_router(login.router, prefix="/api", tags=["login"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(user_details.router, prefix="/api", tags=["user-details"])
# roles need to be implemented to restrict access
# app.include_router(users.router, prefix="/api", tags=["admin"])

app = app_util.set_openapi_info(app=app)
