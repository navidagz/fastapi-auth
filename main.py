import types

from fastapi import FastAPI
from fastapi import Request

from config.fastapi_users import fastapi_users
from config.jwt import jwt_authentication
from config.settings import settings
from db.schema import UserDB
from routers.v1.auth import get_refresh_token_router

app = FastAPI()


# ## Override this
def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


AUTH_V1_PREFIX = "/v1/auth"
# Register
app.include_router(
    fastapi_users.get_register_router(),
    prefix=AUTH_V1_PREFIX,
    tags=["auth"],
)
# Login
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix=AUTH_V1_PREFIX,
    tags=["auth"],
)
# Request verify/verify
app.include_router(
    fastapi_users.get_verify_router(settings.secret, after_verification_request=after_verification_request),
    prefix=AUTH_V1_PREFIX,
    tags=["auth"],
)
# Manage users
app.include_router(
    fastapi_users.get_users_router(requires_verification=True),
    prefix="/v1/users",
    tags=["users"],
)

# Refresh token
fastapi_users.get_refresh_token = types.MethodType(get_refresh_token_router, fastapi_users)
app.include_router(
    fastapi_users.get_refresh_token(jwt_authentication, requires_verification=True),
    prefix=AUTH_V1_PREFIX
)
