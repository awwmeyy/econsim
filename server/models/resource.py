# models/resource.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class Resource(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    # Market properties
    base_price = Column(Numeric, nullable=False)
    current_price = Column(Numeric, nullable=False)
    quantity_threshold = Column(Integer, nullable=False)
    max_transaction_per_turn = Column(Integer, nullable=False)
    max_price = Column(Numeric, nullable=False)
    min_price = Column(Numeric, nullable=False)
    # Relationships
    industry_inputs = relationship('IndustryInput', back_populates='resource')
    industry_outputs = relationship('IndustryOutput', back_populates='resource')
    stockpiles = relationship('Stockpile', back_populates='resource')
    natural_resources = relationship('NaturalResource', back_populates='resource')
    transactions = relationship('MarketTransaction', back_populates='resource')
    market_prices = relationship('MarketPrice', back_populates='resource')

class IndustryInput(Base):
    __tablename__ = 'industry_inputs'

    id = Column(Integer, primary_key=True)
    industry_id = Column(Integer, ForeignKey('industries.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    # Quantity per production cycle at current production level
    quantity = Column(Integer, nullable=False)
    # Relationships
    industry = relationship('Industry', back_populates='inputs')
    resource = relationship('Resource', back_populates='industry_inputs')

class IndustryOutput(Base):
    __tablename__ = 'industry_outputs'

    id = Column(Integer, primary_key=True)
    industry_id = Column(Integer, ForeignKey('industries.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    # Quantity per production cycle at current production level
    quantity = Column(Integer, nullable=False)
    # Relationships
    industry = relationship('Industry', back_populates='outputs')
    resource = relationship('Resource', back_populates='industry_outputs')
