from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user
from auth.models import User

router = APIRouter()

@router.get("/index")
async def read_index(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! Welcome to the protected index route."}
