from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(
    tags=["User Account"],
    prefix="User"
)


@router.get("/user")
def get_user():
    return