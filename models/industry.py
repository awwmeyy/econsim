# models/industry.py
from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey, Numeric, Text, Boolean
)
from sqlalchemy.orm import relationship
from .base import Base

class Industry(Base):
    __tablename__ = 'industries'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    industry_id = Column(String, nullable=False)
    type = Column(Enum('Primary', 'Secondary', 'Tertiary', name='industry_type'), nullable=False)
    sub_type = Column(String, nullable=False)
    production_level = Column(Integer, nullable=False)
    technology_level = Column(Integer, nullable=False)
    # Workforce employed after technology reductions
    skilled_workers_employed = Column(Integer, nullable=False)
    unskilled_workers_employed = Column(Integer, nullable=False)
    # Relationships
    country = relationship('Country', back_populates='industries')
    inputs = relationship('IndustryInput', back_populates='industry')
    outputs = relationship('IndustryOutput', back_populates='industry')
    technology_upgrades = relationship('TechnologyUpgrade', back_populates='industry')
    expansions = relationship('IndustryExpansion', back_populates='industry')

class TechnologyUpgrade(Base):
    __tablename__ = 'technology_upgrades'

    id = Column(Integer, primary_key=True)
    industry_id = Column(Integer, ForeignKey('industries.id'), nullable=False)
    initiated_turn_id = Column(Integer, ForeignKey('turns.id'), nullable=False)
    new_technology_level = Column(Integer, nullable=False)
    upgrade_cost = Column(Numeric, nullable=False)
    total_time_required = Column(Integer, nullable=False)
    remaining_time = Column(Integer, nullable=False)  # Decrements each turn
    benefits = Column(Text, nullable=True)  # JSON string
    is_completed = Column(Boolean, default=False)
    # Relationships
    industry = relationship('Industry', back_populates='technology_upgrades')
    initiated_turn = relationship('Turn')  # Assuming you might want to access the turn

class IndustryExpansion(Base):
    __tablename__ = 'industry_expansions'

    id = Column(Integer, primary_key=True)
    industry_id = Column(Integer, ForeignKey('industries.id'), nullable=False)
    initiated_turn_id = Column(Integer, ForeignKey('turns.id'), nullable=False)
    new_production_level = Column(Integer, nullable=False)
    expansion_cost = Column(Numeric, nullable=False)
    total_time_required = Column(Integer, nullable=False)
    remaining_time = Column(Integer, nullable=False)  # Decrements each turn
    additional_skilled_workers_required = Column(Integer, nullable=False)
    additional_unskilled_workers_required = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)
    # Relationships
    industry = relationship('Industry', back_populates='expansions')
    initiated_turn = relationship('Turn')  # Assuming you might want to access the turn
