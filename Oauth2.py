from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils import verify_access_token, verify_refresh_token
from sqlalchemy.orm import Session
from database import get_db
import models
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
   payload = verify_access_token(token)
   username : str = payload.get("sub")
   user = db.query(models.User).filter(models.User.username == username).first()
   if user is None:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="User not found",
           headers = {"WWW-Authenticate": "Bearer"}
           )
   return user
def get_current_admin(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to access this resource" ,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
