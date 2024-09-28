# models/market.py
from sqlalchemy import Column, Integer, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class MarketPrice(Base):
    __tablename__ = 'market_prices'

    id = Column(Integer, primary_key=True)
    turn_id = Column(Integer, ForeignKey('turns.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    price = Column(Numeric, nullable=False)
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('turn_id', 'resource_id', name='_turn_resource_price_uc'),
    )
    # Relationships
    turn = relationship('Turn', back_populates='market_prices')
    resource = relationship('Resource', back_populates='market_prices')
