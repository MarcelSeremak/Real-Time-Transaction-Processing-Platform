from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

if TYPE_CHECKING:
    from db.models.transaction import Transaction


class Merchant(Base):
    __tablename__ = "merchants"

    merchant_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    risk_level: Mapped[str] = mapped_column(nullable=False)
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="merchant"
    )