from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from auth.models import User
from auth.dependencies import get_db

router = APIRouter()

@router.get("/index")
async def read_index(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.email}! Welcome to the protected index route."}

# Existing routes for login, logout, password recovery...
