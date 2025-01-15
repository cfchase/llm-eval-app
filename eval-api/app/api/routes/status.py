from fastapi import APIRouter


router = APIRouter(
    prefix="/status",
    responses={404: {"description": "Not found"}},
)


@router.get("")
@router.get("/")
async def read_status():
    return {"status": "ok"}
