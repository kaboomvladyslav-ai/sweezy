from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import Token
from ..services import AuthService


router = APIRouter()


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    token = AuthService.authenticate_admin(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return Token(access_token=token)


