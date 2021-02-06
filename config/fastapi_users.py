from fastapi_users import FastAPIUsers

from config.jwt import jwt_authentication
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
