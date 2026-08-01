from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base

if TYPE_CHECKING:
    from db.models.account import Account


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    risk_level: Mapped[str] = mapped_column(nullable=False)
    registration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    status: Mapped[str] = mapped_column(nullable=False)
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        back_populates="customer"
    )