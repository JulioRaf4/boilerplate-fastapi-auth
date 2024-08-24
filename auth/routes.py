from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.dependencies import get_current_user
from auth.utils import verify_password, create_access_token, get_password_hash
from auth.schema import Token, UserCreate, UserOut
from db.connection import get_user_collection
from db.models import UserModel

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_collection = get_user_collection()
    user = await user_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/logout", response_model=dict)
async def logout(current_user: dict = Depends(get_current_user)):
    return {"message": f"User {current_user['email']} successfully logged out"}

@router.post("/password-recovery")
async def password_recovery(email: str):
    user_collection = get_user_collection()
    user = await user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    # Send password recovery email (implementation depends on your strategy)
    return {"message": "Password recovery email sent"}

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    user_collection = get_user_collection()

    # Check if the user already exists
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Hash the user's password
    hashed_password = get_password_hash(user.password)

    # Create a new user document
    new_user = UserModel(
        email=user.email,
        hashed_password=hashed_password,
    )

    # Insert the new user into the MongoDB collection
    result = await user_collection.insert_one(new_user.dict(by_alias=True))
    created_user = await user_collection.find_one({"_id": result.inserted_id})

    return created_user
