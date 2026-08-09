from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

if TYPE_CHECKING:
    from db.models.account import Account
    from db.models.merchant import Merchant


class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )
    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("accounts.account_id"),
        nullable=False
    )
    merchant_id: Mapped[UUID] = mapped_column(
        ForeignKey("merchants.merchant_id"),
        nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )
    currency: Mapped[str] = mapped_column(nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )
    status: Mapped[str] = mapped_column(nullable=False)
    fraud_score: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )
    account: Mapped["Account"] = relationship(
        "Account",
        back_populates="transactions"
    )
    merchant: Mapped["Merchant"] = relationship(
        "Merchant",
        back_populates="transactions"
    )