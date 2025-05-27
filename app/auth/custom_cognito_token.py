from fastapi_cognito import CognitoToken
from typing import Optional

class CustomCognitoToken(CognitoToken):
    scope: Optional[str] = None # type: ignore
    client_id: Optional[str] = None # type: ignore
    username: Optional[str] = None # type: ignore