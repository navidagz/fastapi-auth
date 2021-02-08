from fastapi import Request

from db.schema import UserDB
from fastapi import Request

from db.schema import UserDB


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification link: http://0.0.0.0:8000/v1/auth/verify-account?token={token}")


def after_verification(user: UserDB, request: Request):
    print(f"{user.id} is now verified.")
