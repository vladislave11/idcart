from fastapi import FastAPI
from database import create_db
from user.routes import router as user_router
from admin_panel.routes import router as admin_router


app = FastAPI()

create_db()

app.include_router(user_router)
app.include_router(admin_router)





