import os
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

security = HTTPBearer()


def validate_session_with_supabase(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        # Validate the session ID with Supabase
        user = supabase.auth.get_user(credentials.credentials)
        return
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )