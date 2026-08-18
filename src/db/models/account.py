from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

if TYPE_CHECKING:
    from db.models.customer import Customer


class Account(Base):
    __tablename__ = "accounts"

    account_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()")
    )
    customer_id: Mapped[UUID] = mapped_column(ForeignKey("customers.customer_id"))
    iban: Mapped[str] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=text("now()"),
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        nullable=False
    )
    customer: Mapped["Customer"] = relationship(
        "Customer",
        back_populates="accounts"
    )