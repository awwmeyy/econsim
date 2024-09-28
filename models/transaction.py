# models/transaction.py
from sqlalchemy import Column, Integer, Enum, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class MarketTransaction(Base):
    __tablename__ = 'market_transactions'

    id = Column(Integer, primary_key=True)
    turn_id = Column(Integer, ForeignKey('turns.id'), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    transaction_type = Column(Enum('Buy', 'Sell', name='transaction_type'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Numeric, nullable=False)
    total_price = Column(Numeric, nullable=False)
    # Relationships
    turn = relationship('Turn', back_populates='market_transactions')
    country = relationship('Country', back_populates='transactions')
    resource = relationship('Resource', back_populates='transactions')
