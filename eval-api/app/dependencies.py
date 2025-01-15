from app.utils.config import logger

from typing import Annotated
from fastapi import Header, HTTPException


async def get_token_header():
    logger.info("Root endpoint accessed")
    return

# async def get_token_header(bearer_token: Annotated[str, Header()]):
#     logger.info(bearer_token)
#     # if x_token != "fake-super-secret-token":
#     #     raise HTTPException(status_code=400, detail="X-Token header invalid")
