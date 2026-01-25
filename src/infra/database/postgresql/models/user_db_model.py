from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, Integer, Text
from datetime import datetime, timezone

class Users(UpdateFromSchemaMixin, Base):
    __tablename__ = 'users'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    chat_id = Column(Text, unique=True, nullable=False)
    tokens = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
