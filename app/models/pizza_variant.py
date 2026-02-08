from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PizzaVariant(Base):
    __tablename__ = "pizza_variants"

    id: Mapped[int] = mapped_column(primary_key=True)

    pizza_id: Mapped[int] = mapped_column(
        ForeignKey("pizzas.id", ondelete="CASCADE")
    )

    size: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    pizza = relationship(
        "Pizza",
        back_populates="variants"
    )
