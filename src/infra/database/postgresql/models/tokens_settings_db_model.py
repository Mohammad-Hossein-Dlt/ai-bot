from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, Integer, Text
from datetime import datetime, timezone
    
class TokenSettings(UpdateFromSchemaMixin, Base):
    __tablename__ = 'token_settings'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    tokens_per_prompt = Column(Integer, nullable=False, default=0)
    unit = Column(Integer, nullable=False, default=0)
    min = Column(Integer, nullable=False, default=0)
    max = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
