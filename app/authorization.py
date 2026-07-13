from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

SECRET_API_KEY = "i_have_to_write_something_here"
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)

def check_api_key(api_key_from_header: str = Depends(API_KEY_HEADER)):
    if api_key_from_header != SECRET_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API Key is incorrect")
    return api_key_from_header