import types

from fastapi_users import FastAPIUsers

from config.jwt import jwt_authentication
from db.init import user_db
from db.schema import User, UserDB, UserUpdate, UserCreate
from routers.v1.auth import get_refresh_token_router, get_verify_account_router

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
fastapi_users.get_refresh_token = types.MethodType(get_refresh_token_router, fastapi_users)
fastapi_users.get_verify_account = types.MethodType(get_verify_account_router, fastapi_users)
