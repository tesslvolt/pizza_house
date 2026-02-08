from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )

    pizza_variant_id: Mapped[int] = mapped_column(
        ForeignKey("pizza_variants.id", ondelete="CASCADE"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    order = relationship(
        "Order",
        back_populates="items"
    )

    pizza_variant = relationship(
        "PizzaVariant"
    )
