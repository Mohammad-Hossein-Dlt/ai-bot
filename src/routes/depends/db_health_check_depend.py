# from fastapi import Depends
from .depend import inject, Depends
from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from .db_depend import db_depend
from sqlalchemy import text

@inject
async def db_health_check_depend(
    db: AsyncMongoClient | Session = Depends(db_depend)
):
    if isinstance(db, Session):
        try:
            request = db.execute(text("SELECT 1"))
            _ = request.scalar()
            return True
        except:
            db.rollback()
            return False
    
    if isinstance(db, AsyncMongoClient):
        try:
            await db.admin.command("ping")
            return True
        except Exception:
            return False