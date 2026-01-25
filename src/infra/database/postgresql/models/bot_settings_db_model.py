from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, Integer, Boolean
from datetime import datetime, timezone

class BotSettings(UpdateFromSchemaMixin, Base):
    __tablename__ = 'bot_settings'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
