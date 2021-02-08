from typing import Callable, Optional, cast

import jwt
from fastapi import APIRouter, HTTPException, Request, status
from fastapi_users import models
from fastapi_users.router.common import ErrorCode, run_handler
from fastapi_users.user import (
    UserAlreadyVerified,
    UserNotExists,
)
from fastapi_users.utils import JWT_ALGORITHM
from pydantic import UUID4, EmailStr

VERIFY_USER_TOKEN_AUDIENCE = "fastapi-users:verify"


def get_verify_account_router(
        self,
        verification_token_secret: str,
        after_verification: Optional[Callable[[models.UD, Request], None]] = None,
):
    router = APIRouter()

    @router.get("/verify-account", response_model=self._user_model)
    async def verify(request: Request, token: str):
        try:
            data = jwt.decode(
                token,
                verification_token_secret,
                audience=VERIFY_USER_TOKEN_AUDIENCE,
                algorithms=[JWT_ALGORITHM],
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_TOKEN_EXPIRED,
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
            )

        user_id = data.get("user_id")
        email = cast(EmailStr, data.get("email"))

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
            )

        try:
            user_check = await self.get_user(email)
        except UserNotExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
            )

        try:
            user_uuid = UUID4(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
            )

        if user_check.id != user_uuid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
            )

        try:
            user = await self.verify_user(user_check)
        except UserAlreadyVerified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
            )

        if after_verification:
            await run_handler(after_verification, user, request)

        return user

    return router
