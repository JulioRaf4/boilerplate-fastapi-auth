from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from auth.schema import TokenData
from auth.utils import SECRET_KEY, ALGORITHM
from db.connection import get_user_collection  # Corrected import path
import logging


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    logging.info(f"Token received: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logging.info(f"Token payload: {payload}")
        email: str = payload.get("sub")
        if email is None:
            logging.error("Email not found in token.")
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError as e:
        logging.error(f"JWTError: {e}")
        raise credentials_exception

    user_collection = get_user_collection()
    user = await user_collection.find_one({"email": token_data.email})
    if user is None:
        logging.error("User not found.")
        raise credentials_exception
    logging.info(f"User authenticated: {user['email']}")
    return user
