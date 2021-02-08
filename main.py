import types

from fastapi import FastAPI

from config.after_actions import after_verification, after_verification_request
from config.fastapi_users import fastapi_users
from config.jwt import jwt_authentication
from config.route_prefix import AUTH_V1_PREFIX, AUTH_TAGS, USERS_V1_PREFIX, USERS_TAGS
from config.settings import settings
from routers.v1.auth import get_refresh_token_router, get_verify_account_router

app = FastAPI()

# Register
app.include_router(
    fastapi_users.get_register_router(),
    prefix=AUTH_V1_PREFIX,
    tags=AUTH_TAGS
)
# Login
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix=AUTH_V1_PREFIX,
    tags=AUTH_TAGS
)

# Request verify
request_verification_router = fastapi_users.get_verify_router(
    settings.secret,
    after_verification_request=after_verification_request
)
request_verification_router.routes = [route for route in request_verification_router.routes if route.name != "verify"]
app.include_router(
    request_verification_router,
    prefix=AUTH_V1_PREFIX,
    tags=AUTH_TAGS
)

# Verify Account
fastapi_users.get_verify_account = types.MethodType(get_verify_account_router, fastapi_users)
app.include_router(
    fastapi_users.get_verify_account(settings.secret, after_verification=after_verification),
    prefix=AUTH_V1_PREFIX,
    tags=AUTH_TAGS
)

# Refresh token
fastapi_users.get_refresh_token = types.MethodType(get_refresh_token_router, fastapi_users)
app.include_router(
    fastapi_users.get_refresh_token(jwt_authentication, requires_verification=True),
    prefix=AUTH_V1_PREFIX,
    tags=AUTH_TAGS
)

# Manage users
app.include_router(
    fastapi_users.get_users_router(requires_verification=True),
    prefix=USERS_V1_PREFIX,
    tags=USERS_TAGS
)
