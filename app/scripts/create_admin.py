import asyncio

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User
from sqlalchemy import select


async def create_admin():
    async with AsyncSessionLocal() as session:
        admin_email = "admin@example.com"
        admin_password = "admin123"

        result = await session.execute(
            select(User).where(User.email == admin_email)
        )
        existing = result.scalar_one_or_none()

        if existing:
            print("❗ Админ уже существует")
            return

        admin = User(
            email=admin_email,
            hashed_password=get_password_hash(admin_password),
            is_admin=True
        )

        session.add(admin)
        await session.commit()

        print("✅ Админ создан")
        print("email:", admin_email)
        print("password:", admin_password)

if __name__ == "__main__":
    asyncio.run(create_admin())
