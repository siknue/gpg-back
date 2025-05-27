import os
from dotenv import load_dotenv
from fastapi_cognito import CognitoSettings, CognitoAuth
from app.auth.custom_cognito_token import CustomCognitoToken

load_dotenv()

cognito_settings = CognitoSettings(
    jwt_header_prefix= "Bearer",
    jwt_header_name = "Authorization",
    check_expiration=False,
    userpools = {
        "default":{
            "region":os.getenv("AWS_REGION", "ap-northeast-1"),
            "userpool_id":os.getenv("COGNITO_USERPOOL_ID"),
            "app_client_id":os.getenv("COGNITO_APP_CLIENT_ID"),
        }
    }
)

cognito_auth = CognitoAuth(
    settings=cognito_settings,
    custom_model=CustomCognitoToken
)