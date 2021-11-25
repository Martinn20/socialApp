from fastapi import *
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Token
from .. import models, oauth2
from ..utils import hash, verify


router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")

    access_token = oauth2.create_access_token(data={"user_email": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

