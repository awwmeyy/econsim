# models/game.py
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    current_turn_number = Column(Integer, default=1)
    total_turns = Column(Integer, default=50)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    # Relationships
    user = relationship('User', back_populates='games')
    countries = relationship('Country', back_populates='game')
    turns = relationship('Turn', back_populates='game', order_by='Turn.turn_number')

class Turn(Base):
    __tablename__ = 'turns'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    turn_number = Column(Integer, nullable=False)
    # Relationships
    game = relationship('Game', back_populates='turns')
    actions = relationship('Action', back_populates='turn')
    market_transactions = relationship('MarketTransaction', back_populates='turn')
    market_prices = relationship('MarketPrice', back_populates='turn')
