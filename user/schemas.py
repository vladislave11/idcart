from pydantic import BaseModel
from typing import List, Any


class UserCreate(BaseModel):
    isikukood: str
    email: str
    password: str


