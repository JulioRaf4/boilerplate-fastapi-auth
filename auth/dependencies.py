from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .models import User
from .schema import TokenData
from .utils import SECRET_KEY, ALGORITHM
from .database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user
