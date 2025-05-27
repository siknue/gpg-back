from fastapi import APIRouter, Depends

from app.auth.cognito_auth import cognito_auth
from app.auth.custom_cognito_token import CustomCognitoToken

router = APIRouter()

@router.get("/auth_health")
def secure_endpoint(auth: CustomCognitoToken = Depends(cognito_auth.auth_required)):
    return{
        "message":"Hello, this is a secure endpoint!",
        "claims": auth.model_dump()
    }