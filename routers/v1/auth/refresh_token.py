from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from fastapi_users.authentication import BaseAuthentication
from fastapi_users.router.common import ErrorCode


def get_refresh_token_router(
        self,
        backend: BaseAuthentication,
        requires_verification: bool = False, ) -> APIRouter:
    router = APIRouter()

    if requires_verification:
        get_current_active_user = self.authenticator.get_current_verified_user
    else:
        get_current_active_user = self.authenticator.get_current_active_user

    @router.post("/refresh-token")
    async def refresh_token(
            user: self._user_db_model = Depends(get_current_active_user),
    ):
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )
        if requires_verification and not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
            )
        return await backend.get_login_response(user, None)

    return router
