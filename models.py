from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB

from database_setup import Base


class InputItem(Base):
    """Model for input data"""
    __tablename__ = 'input'

    id = Column('id', Integer, primary_key=True)
    data = Column('data', JSONB)

    def __init__(self, data):
        super().__init__()
        self.data = data