from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginRequest
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.crud.user_crud import get_user_by_email, get_user_by_id, create_user

router = APIRouter( tags=["Auth"])


@router.post("/login")
async def login(
    response: Response,
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,       # True на проде (HTTPS)
        samesite="lax",
        max_age=60*60       # 1 час
    )

    return {"is_admin": user.is_admin, "message": "Login successful"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@router.get("/me")
async def get_current_user(
    access_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    from app.core.security import decode_access_token
    try:
        payload = decode_access_token(access_token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "is_admin": user.is_admin
    }

@router.post("/register")
async def register(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    hashed_password = get_password_hash(data.password)
    user = await create_user(db, email=data.email, hashed_password=hashed_password)

    return {"message": "Регистрация успешна", "user_id": user.id}