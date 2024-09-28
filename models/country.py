# models/country.py
from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    name = Column(String, nullable=False)
    is_ai = Column(Boolean, default=True)
    government_capital = Column(Numeric, nullable=False)
    # Workforce
    total_skilled_workers = Column(Integer, nullable=False)
    total_unskilled_workers = Column(Integer, nullable=False)
    unemployed_skilled_workers = Column(Integer, nullable=False)
    unemployed_unskilled_workers = Column(Integer, nullable=False)
    # Relationships
    game = relationship('Game', back_populates='countries')
    industries = relationship('Industry', back_populates='country')
    stockpiles = relationship('Stockpile', back_populates='country')
    natural_resources = relationship('NaturalResource', back_populates='country')
    actions = relationship('Action', back_populates='country')
    transactions = relationship('MarketTransaction', back_populates='country')

class Stockpile(Base):
    __tablename__ = 'stockpiles'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('country_id', 'resource_id', name='_country_resource_uc'),
    )
    # Relationships
    country = relationship('Country', back_populates='stockpiles')
    resource = relationship('Resource', back_populates='stockpiles')

class NaturalResource(Base):
    __tablename__ = 'natural_resources'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    total_reserves = Column(Integer, nullable=False)
    extraction_rate = Column(Integer, nullable=False)
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('country_id', 'resource_id', name='_country_resource_natural_uc'),
    )
    # Relationships
    country = relationship('Country', back_populates='natural_resources')
    resource = relationship('Resource', back_populates='natural_resources')
