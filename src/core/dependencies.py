from typing import Annotated

from fastapi import Depends, HTTPException

from src.core import models
from src.core.database import GetDBDep
from src.service.auth import oauth2_scheme, verify_token


def get_current_user(
        db: GetDBDep, token: Annotated[str, Depends(oauth2_scheme)]
):
    email = verify_token(token)

    print("EMAIL", email)

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user