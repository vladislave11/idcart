from pydantic import BaseModel, Field


class UpdateUserSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    citizenship: str = Field(..., min_length=1, max_length=100)
    gender: str = Field(..., min_length=1, max_length=10)


class UserDeleteSchema(BaseModel):
    isikukood: str = Field(..., min_length=11, max_length=11)
