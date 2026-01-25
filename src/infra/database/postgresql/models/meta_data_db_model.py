from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, Integer, Text
from datetime import datetime, timezone
    
class MetaData(UpdateFromSchemaMixin, Base):
    __tablename__ = 'meta_data'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    channel_id = Column(Text, nullable=False)
    support_id = Column(Text, nullable=False)
    bot_id = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

