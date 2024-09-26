from typing import Optional
from datetime import date
from pydantic import BaseModel, Field
from fastapi import UploadFile


class UpdateUserSchema(BaseModel):
    isikukood: str = Field(..., min_length=11, max_length=11)
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    citizenship: str = Field(..., min_length=1, max_length=100)
    gender: str = Field(..., min_length=1, max_length=10)
    photo: Optional[UploadFile] = None


class UserDeleteSchema(BaseModel):
    isikukood: str = Field(..., min_length=11, max_length=11)
