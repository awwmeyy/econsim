from sqlalchemy import (
    create_engine, Column, Integer, String, Float, ForeignKey, Enum,
    Boolean, DateTime, Numeric, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    # Relationships
    games = relationship('Game', backref='user')

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    current_turn_number = Column(Integer, default=1)
    total_turns = Column(Integer, default=50)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    # Relationships
    countries = relationship('Country', backref='game')
    turns = relationship('Turn', backref='game', order_by='Turn.turn_number')

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
    industries = relationship('Industry', backref='country')
    stockpiles = relationship('Stockpile', backref='country')
    natural_resources = relationship('NaturalResource', backref='country')
    actions = relationship('Action', backref='country')
    transactions = relationship('MarketTransaction', backref='country')

class Turn(Base):
    __tablename__ = 'turns'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    turn_number = Column(Integer, nullable=False)
    # Relationships
    actions = relationship('Action', backref='turn')
    market_transactions = relationship('MarketTransaction', backref='turn')
    market_prices = relationship('MarketPrice', backref='turn')

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
    industry_inputs = relationship('IndustryInput', backref='resource')
    industry_outputs = relationship('IndustryOutput', backref='resource')
    stockpiles = relationship('Stockpile', backref='resource')
    natural_resources = relationship('NaturalResource', backref='resource')
    transactions = relationship('MarketTransaction', backref='resource')
    market_prices = relationship('MarketPrice', backref='resource')


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
    inputs = relationship('IndustryInput', backref='industry')
    outputs = relationship('IndustryOutput', backref='industry')
    # Ongoing upgrades and actions
    technology_upgrades = relationship('TechnologyUpgrade', backref='industry')
    expansions = relationship('IndustryExpansion', backref='industry')

class IndustryInput(Base):
    __tablename__ = 'industry_inputs'

    id = Column(Integer, primary_key=True)
    industry_id = Column(Integer, ForeignKey('industries.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    # Quantity per production cycle at current production level
    quantity = Column(Integer, nullable=False)

class IndustryOutput(Base):
    __tablename__ = 'industry_outputs'

    id = Column(Integer, primary_key=True)
    industry_id = Column(Integer, ForeignKey('industries.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    # Quantity per production cycle at current production level
    quantity = Column(Integer, nullable=False)

class Stockpile(Base):
    __tablename__ = 'stockpiles'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    # Unique constraint to prevent duplicate entries per country-resource
    __table_args__ = (
        UniqueConstraint('country_id', 'resource_id', name='_country_resource_uc'),
    )

class NaturalResource(Base):
    __tablename__ = 'natural_resources'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    total_reserves = Column(Integer, nullable=False)
    extraction_rate = Column(Integer, nullable=False)
    # Unique constraint to prevent duplicate entries per country-resource
    __table_args__ = (
        UniqueConstraint('country_id', 'resource_id', name='_country_resource_natural_uc'),
    )

class MarketPrice(Base):
    __tablename__ = 'market_prices'

    id = Column(Integer, primary_key=True)
    turn_id = Column(Integer, ForeignKey('turns.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    price = Column(Numeric, nullable=False)
    # Unique constraint to prevent duplicate entries per turn-resource
    __table_args__ = (
        UniqueConstraint('turn_id', 'resource_id', name='_turn_resource_price_uc'),
    )

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

class Action(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True)
    turn_id = Column(Integer, ForeignKey('turns.id'), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    type = Column(String, nullable=False)
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'action'
    }

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


class TechnologyUpgrade(Base):
    __tablename__ = 'technology_upgrades'

    id = Column(Integer, primary_key=True)
    industry_id = Column(Integer, ForeignKey('industries.id'), nullable=False)
    initiated_turn_id = Column(Integer, ForeignKey('turns.id'), nullable=False)
    new_technology_level = Column(Integer, nullable=False)
    upgrade_cost = Column(Numeric, nullable=False)
    total_time_required = Column(Integer, nullable=False)
    remaining_time = Column(Integer, nullable=False)  # Decrements each turn
    benefits = Column(Text)  # JSON string
    is_completed = Column(Boolean, default=False)

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
