from importlib.metadata import metadata
from sqlalchemy import Column, Integer, DateTime, MetaData

from quiz_project import Base
from quiz_project import get_current_time


class AbstractBaseModel(Base):
    __abstract__ = True
    metadata = MetaData()

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=get_current_time)
    updated_at = Column(DateTime(timezone=True), onupdate=get_current_time)
