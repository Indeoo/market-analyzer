from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Token(Base):
    __tablename__ = 'tokens'

    address = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    decimals = Column(Integer, nullable=False)
    logo_uri = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)  # JSON field to store tags as a list
    daily_volume = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False)
    freeze_authority = Column(String, nullable=True)
    mint_authority = Column(String, nullable=True)
    permanent_delegate = Column(String, nullable=True)
    minted_at = Column(DateTime, nullable=True)
    extensions = Column(JSON, nullable=True)  # JSON field to store extensions

    def __repr__(self):
        return f"<Token(address='{self.address}', name='{self.name}', symbol='{self.symbol}')>"
