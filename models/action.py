# models/action.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Numeric, Text
from sqlalchemy.orm import relationship
from .base import Base

class Action(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True)
    turn_id = Column(Integer, ForeignKey('turns.id'), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    type = Column(String, nullable=False)
    # Polymorphic configuration
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'action'
    }
    # Relationships
    turn = relationship('Turn', back_populates='actions')
    country = relationship('Country', back_populates='actions')

class StartNewIndustryAction(Action):
    __tablename__ = 'start_new_industry_actions'
    id = Column(Integer, ForeignKey('actions.id'), primary_key=True)
    selected = Column(Boolean, default=False)  # Indicates if the action has been selected by the player/AI
    industry_id = Column(String, nullable=False)
    industry_type = Column(Enum('Primary', 'Secondary', 'Tertiary', name='industry_type'), nullable=False)
    sub_type = Column(String, nullable=False)
    setup_cost = Column(Numeric, nullable=False)
    production_level = Column(Integer, nullable=False)
    technology_level = Column(Integer, nullable=False)
    inputs_required = Column(Text)  # JSON string
    outputs_produced = Column(Text)  # JSON string
    skilled_workers_required = Column(Integer, nullable=False)
    unskilled_workers_required = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'StartNewIndustry',
    }

class ExpandIndustryAction(Action):
    __tablename__ = 'expand_industry_actions'
    id = Column(Integer, ForeignKey('actions.id'), primary_key=True)
    selected = Column(Boolean, default=False)
    industry_id = Column(Integer, ForeignKey('industries.id'), nullable=False)
    new_production_level = Column(Integer, nullable=False)
    expansion_cost = Column(Numeric, nullable=False)
    additional_skilled_workers_required = Column(Integer, nullable=False)
    additional_unskilled_workers_required = Column(Integer, nullable=False)
    increase_in_outputs = Column(Text)  # JSON string
    additional_inputs_required = Column(Text)  # JSON string

    __mapper_args__ = {
        'polymorphic_identity': 'ExpandIndustry',
    }

class UpgradeTechnologyAction(Action):
    __tablename__ = 'upgrade_technology_actions'
    id = Column(Integer, ForeignKey('actions.id'), primary_key=True)
    selected = Column(Boolean, default=False)
    industry_id = Column(Integer, ForeignKey('industries.id'), nullable=False)
    new_technology_level = Column(Integer, nullable=False)
    upgrade_cost = Column(Numeric, nullable=False)
    time_to_complete = Column(Integer, nullable=False)
    benefits = Column(Text)  # Description of benefits

    __mapper_args__ = {
        'polymorphic_identity': 'UpgradeTechnology',
    }
