from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, Integer, Text, Boolean
from datetime import datetime, timezone

class Payment(UpdateFromSchemaMixin, Base):
    __tablename__ = 'payment'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Text, nullable=False, default=0)
    chat_id = Column(Text, nullable=False, default=0)
    payment_id = Column(Text, nullable=False, default=0)
    authority = Column(Text, nullable=False, default=0)
    ref_id = Column(Text, nullable=False, default=0)
    amount = Column(Integer, nullable=False, default=0)
    tokens = Column(Integer, nullable=False, default=0)
    status = Column(Boolean, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))