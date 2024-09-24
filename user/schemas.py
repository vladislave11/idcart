from typing import Optional
from pydantic import BaseModel, Field, validator
from fastapi import UploadFile, File


class RegisterUser(BaseModel):
    isikukood: str = Field(..., min_length=11, max_length=11)
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    date_of_birth: str
    citizenship: str = Field(..., min_length=1, max_length=100)
    gender: str = Field(..., min_length=1, max_length=10)
    photo: Optional[UploadFile] = None
    password: str = Field(..., min_length=8)

    @validator('isikukood')
    def validate_isikukood(cls, value):
        if len(value) != 11:
            raise ValueError("Isikukood must be exactly 11 characters long")
        if not value.isdigit():
            raise ValueError("Isikukood must contain only digits")
        return value


class DeleteAccountRequest(BaseModel):
    isikukood: str
    password: str


class UpdateUser(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    date_of_birth: Optional[str] = None
    citizenship: Optional[str] = None
    gender: Optional[str] = None
    photo: Optional[bytes] = None
    email: Optional[str] = None


class LoginUser(BaseModel):
    isikukood: str
    password: str

    @validator('isikukood')
    def validate_isikukood(cls, value):
        if len(value) != 11:
            raise ValueError("Isikukood must be exactly 11 characters long")
        if not value.isdigit():
            raise ValueError("Isikukood must contain only digits")
        return value


