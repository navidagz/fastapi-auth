from fastapi import Request

from db.schema import UserDB
from config.route_prefix import AUTH_V1_PREFIX


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification link: http://0.0.0.0:8000{AUTH_V1_PREFIX}/verify-account?token={token}")


def after_verification(user: UserDB, request: Request):
    print(f"{user.id} is now verified.")
