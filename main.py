from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Id_Cart, get_db, create_db
from authentication.auth import get_current_user
from user.routes import router as user_router
from admin_panel.routes import router as admin_router


app = FastAPI()

create_db()

app.include_router(user_router)
app.include_router(admin_router)





