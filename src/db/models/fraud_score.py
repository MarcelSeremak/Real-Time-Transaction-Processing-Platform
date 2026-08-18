from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class FraudScore(Base):
    __tablename__ = "fraud_scores"

    transaction_id: Mapped[UUID] = mapped_column(
        ForeignKey("transactions.transaction_id"),
        primary_key=True
    )
    fraud_score: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )
