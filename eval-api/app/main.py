from fastapi import Depends, FastAPI
from app.api.main import api_router
from app.utils.config import app_config, logger
from app.utils.storage import storage

app = FastAPI()
app.include_router(api_router)


@app.get("")
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"root": "Hello World!"}

