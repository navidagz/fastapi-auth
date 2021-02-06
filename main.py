from fastapi import FastAPI
from fastapi import Request
from fastapi_users import FastAPIUsers

from config.jwt import jwt_authentication
from config.settings import settings
from db.init import user_db
from db.schema import User, UserDB, UserUpdate, UserCreate

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
app = FastAPI()


# ## Override this
def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


# Register
app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)
# Login
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth",
    tags=["auth"],
)
# Request verify/verify
app.include_router(
    fastapi_users.get_verify_router(settings.secret, after_verification_request=after_verification_request),
    prefix="/auth",
    tags=["auth"],
)
# Manage users
app.include_router(
    fastapi_users.get_users_router(jwt_authentication, requires_verification=True),
    prefix="/users",
    tags=["users"],
)
