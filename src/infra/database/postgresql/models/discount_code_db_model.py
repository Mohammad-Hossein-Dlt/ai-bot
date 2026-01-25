from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, Integer, Text
from datetime import datetime, timezone

class DiscountCode(UpdateFromSchemaMixin, Base):
    __tablename__ = 'discount_code'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Text, unique=True, nullable=False)
    percent = Column(Integer, nullable=False, default=0)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
