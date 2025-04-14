import os
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import clients as clients

security = HTTPBearer()


def validate_session_with_supabase(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        # Validate the session ID with Supabase
        user = clients.supabase_client.auth.get_user(credentials.credentials)
        return
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )