from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import Id_Cart, get_db
from datetime import date
from user.schemas import LoginUser, DeleteAccountRequest, UpdateUser
from authentication.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()


@router.post("/register/")
async def register(
        isikukood: str,
        name: str,
        surname: str,
        date_of_birth: date,
        citizenship: str,
        gender: str,
        password: str,
        photo: UploadFile = File(...),
        db: Session = Depends(get_db)
):

    hashed_password = hash_password(password)

    existing_user = db.query(Id_Cart).filter(Id_Cart.isikukood == isikukood).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this isikukood already exists")

    photo_data = await photo.read() if photo else None

    new_user = Id_Cart(
        isikukood=isikukood,
        name=name,
        surname=surname,
        date_of_birth=date_of_birth,
        citizenship=citizenship,
        gender=gender,
        photo=photo_data,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully", "isikukood": isikukood}


@router.post("/login/")
async def login(user: LoginUser = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(Id_Cart).filter(Id_Cart.isikukood == user.isikukood).first()
    if existing_user is None or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid isikukood or password")

    access_token = create_access_token(data={"sub": user.isikukood})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
def read_users_me(current_user: Id_Cart = Depends(get_current_user)):
    return {
        "isikukood": current_user.isikukood,
        "name": current_user.username,
        "email": current_user.email,
    }


@router.put("/update/{isikukood}")
async def update_user(isikukood: str, user: UpdateUser, db: Session = Depends(get_db),
                      current_user: Id_Cart = Depends(get_current_user)):
    if current_user.isikukood != isikukood:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    db_user = db.query(Id_Cart).filter(Id_Cart.isikukood == isikukood).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.name = user.name
    db_user.surname = user.surname
    db_user.date_of_birth = user.date_of_birth
    db_user.citizenship = user.citizenship
    db_user.gender = user.gender
    db_user.photo = user.photo
    db_user.password = hash_password(user.password)

    db.commit()
    return {"message": "User updated successfully"}


@router.delete("/users/me")
async def delete_own_account(delete_request: DeleteAccountRequest = Depends(),
                             current_user: Id_Cart = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    if not verify_password(delete_request.password, current_user.password):
        raise HTTPException(status_code=403, detail="Invalid password")
    user = db.query(Id_Cart).filter(Id_Cart.isikukood == int(current_user.isikukood)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "Your account has been deleted successfully"}
