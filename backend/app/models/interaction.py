from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hcp_name: Mapped[str] = mapped_column(String(255), index=True)
    hcp_specialty: Mapped[str] = mapped_column(String(255), default="General")
    interaction_type: Mapped[str] = mapped_column(String(100))
    channel: Mapped[str] = mapped_column(String(100), default="In-person")
    raw_notes: Mapped[str] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text)
    sentiment: Mapped[str] = mapped_column(String(50), default="neutral")
    follow_up_action: Mapped[str] = mapped_column(Text, default="")
    created_by: Mapped[str] = mapped_column(String(255), default="field-rep")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
