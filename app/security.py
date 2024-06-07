from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from passlib.context import CryptContext

SECRET_KEY = "6216430b69dc61fde2931bf5d3b97be50acdca4f8974a611cc8fbc09c6b1e3f4"
ALGORITHM = "HS256"

HASHED_USERNAME = "$2b$12$AT8GzullXobHL61MbhSXMevh56DYGmnsiDaR1FbQy2YArqTKEI0Gm"
HASHED_PASSWORD = "$2b$12$KU4OTzOI6pS1jer/eLlxOOfdGso9nPZfPfb1ttMM/biS9FLYj4yGu"

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authorize(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    # global HASHED_USERNAME, HASHED_PASSWORD
    # if not HASHED_USERNAME:
        # HASHED_USERNAME = pwd_context.hash(credentials.username)
        # HASHED_PASSWORD = pwd_context.hash(credentials.password)
        # print(HASHED_USERNAME)
        # print(HASHED_PASSWORD)
    if pwd_context.verify(credentials.username, HASHED_USERNAME) and pwd_context.verify(
        credentials.password, HASHED_PASSWORD
    ):
        return credentials.username