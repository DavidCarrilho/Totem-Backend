from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.sql.annotation import Annotated

from src.core import models
from src.core.database import GetDBDep
from src.core.dependencies import get_current_user
from src.core.models import User
from src.schemas.user import ChangePasswordData
from src.services.auth import authenticate_user, create_access_token, create_refresh_token, verify_token, \
    verify_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login_for_access_token(
     db: GetDBDep,
     form_data: OAuth2PasswordRequestForm = Depends(),
):
    user: models.User | None = authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/refresh")
def refresh_access_token(refresh_token: Annotated[str, Body(..., embed=True)]):
    email = verify_refresh_token(refresh_token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    new_access_token = create_access_token(data={"sub": email})

    return {"access_token": new_access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/chamge-password", response_model=User)
async def change_password(
        chamge_password_data: ChangePasswordData,
        db: GetDBDep,
        current_user: models.User = Depends(get_current_user),
):
    user = authenticate_user(email=current_user.email, password=chamge_password_data.old_password, db=db)
    db.commit()
    db.refresh(user)
    return user