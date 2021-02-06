from fastapi_users.authentication import JWTAuthentication

from config.settings import settings

auth_backends = []

jwt_authentication = JWTAuthentication(secret=settings.secret, lifetime_seconds=3600)

auth_backends.append(jwt_authentication)
