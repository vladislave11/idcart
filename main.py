from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Id_Cart
from authentication.auth import get_current_user
from database import get_db, create_db

app = FastAPI()

create_db()


@app.get("/users/me")
def read_users_me(current_user: Id_Cart = Depends(get_current_user)):
    return {
        "isikukood": current_user.isikukood,
        "name": current_user.username,
        "email": current_user.email,
    }



