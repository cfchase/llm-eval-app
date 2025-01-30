from app.utils.config import logger, APP_API_KEY

from typing import Optional
from fastapi import Header, HTTPException


async def get_token_header(api_key: Optional[str] = Header(None)):
    if APP_API_KEY and api_key != APP_API_KEY:
        raise HTTPException(status_code=400, detail="header api-key invalid")
