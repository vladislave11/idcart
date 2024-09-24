from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from authentication.auth import get_current_user
from database import Id_Cart, get_db
from admin_panel.schemas import UpdateUserSchema


router = APIRouter(
    tags=["Admin Panel"],
    prefix="/Admin"
)


@router.get("/users/me")
def read_users_me(current_user: Id_Cart = Depends(get_current_user)):
    return {
        "isikukood": current_user.isikukood,
        "name": current_user.username,
        "surname": current_user.surname,
        "email": current_user.email,
        "date_of_birth": current_user.date_of_birth,

    }


@router.put("/users/{isikukood}")
async def update_user(isikukood: str, user_data: UpdateUserSchema, db: Session = Depends(get_db), current_user: Id_Cart = Depends(get_current_user)):
    print(f"User {current_user.username} is updating user with isikukood {isikukood}")

    user = db.query(Id_Cart).filter(Id_Cart.isikukood == isikukood).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = user_data.name
    user.surname = user_data.surname
    user.citizenship = user_data.citizenship
    user.gender = user_data.gender

    db.commit()
    return {"message": "User updated successfully"}


@router.delete("/users/{isikukood}")
async def delete_user(isikukood: str, db: Session = Depends(get_db), current_user: Id_Cart = Depends(get_current_user)):
    print(f"User {current_user.username} is attempting to delete user with isikukood {isikukood}")

    user = db.query(Id_Cart).filter(Id_Cart.isikukood == isikukood).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
