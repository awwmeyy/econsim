# background_logic.py

import json
from sqlalchemy.orm import Session
from models import (
    Game, Country, Industry, Stockpile,
    NaturalResource, 
)
from sqlalchemy import and_

def process_background_logic(game: Game, session: Session, turn_number: int):
    """
    Processes the background logic for each turn:
    - Consumes industry inputs and produces outputs
    - Extracts natural resources
    """
    countries = session.query(Country).filter_by(game_id=game.id).all()
    if not countries:
        print("No countries found for the current game.")
        return

    print(f"Processing background logic for Turn {turn_number}...")

    for country in countries:
        print(f"Processing country: {country.name}")

        # Process industries
        for industry in country.industries:
            process_industry(industry, country, session)

        # Extract natural resources
        for nat_resource in country.natural_resources:
            extract_natural_resource(nat_resource, country, session)

    # Commit the session after processing all countries
    session.commit()
    print(f"Background logic for Turn {turn_number} has been completed.")


def process_industry(industry: Industry, country: Country, session: Session):
    """
    Processes an industry for a country:
    - Consumes inputs
    - Produces outputs
    - Checks for sufficient inputs
    - Adjusts workforce if necessary
    """
    # First, check if the industry can operate (has enough inputs)
    can_operate = True

    # Adjust input requirements based on technology level
    technology_multiplier = 1 - (0.05 * industry.technology_level)  # Assuming 5% reduction per tech level

    for industry_input in industry.inputs:
        resource = industry_input.resource
        required_quantity = industry_input.quantity * industry.production_level * technology_multiplier

        # Get the country's stockpile for this resource
        stockpile = session.query(Stockpile).filter_by(
            country_id=country.id, resource_id=resource.id).first()
        if not stockpile or stockpile.quantity < required_quantity:
            print(f"Industry '{industry.sub_type}' cannot operate due to insufficient input '{resource.name}'.")
            can_operate = False
            break

    if can_operate:
        # Consume inputs
        for industry_input in industry.inputs:
            resource = industry_input.resource
            required_quantity = industry_input.quantity * industry.production_level * technology_multiplier

            stockpile = session.query(Stockpile).filter_by(
                country_id=country.id, resource_id=resource.id).first()
            stockpile.quantity -= required_quantity
            print(f"Consumed {required_quantity} of '{resource.name}' from {country.name}'s stockpile.")

        # Adjust output quantities based on technology level
        output_multiplier = 1 + (0.05 * industry.technology_level)  # Assuming 5% increase per tech level

        # Produce outputs
        for industry_output in industry.outputs:
            resource = industry_output.resource
            produced_quantity = industry_output.quantity * industry.production_level * output_multiplier

            # Get or create the country's stockpile for this resource
            stockpile = session.query(Stockpile).filter_by(
                country_id=country.id, resource_id=resource.id).first()
            if not stockpile:
                # Create a new stockpile
                stockpile = Stockpile(country_id=country.id, resource_id=resource.id, quantity=0)
                session.add(stockpile)
                session.flush()
            stockpile.quantity += produced_quantity
            print(f"Produced {produced_quantity} of '{resource.name}' and added to {country.name}'s stockpile.")

    else:
        print(f"Industry '{industry.sub_type}' did not operate this turn due to insufficient inputs.")


def extract_natural_resource(nat_resource: NaturalResource, country: Country, session: Session):
    """
    Extracts a natural resource for a country, up to the extraction rate and total reserves.
    Adds the extracted amount to the country's stockpile.
    """
    # Determine how much can be extracted this turn
    extraction_rate = nat_resource.extraction_rate
    total_reserves = nat_resource.total_reserves

    if total_reserves <= 0:
        print(f"Natural resource '{nat_resource.resource.name}' has been depleted in {country.name}.")
        return

    extracted_quantity = min(extraction_rate, total_reserves)
    nat_resource.total_reserves -= extracted_quantity

    # Add to country's stockpile
    resource = nat_resource.resource

    stockpile = session.query(Stockpile).filter_by(
        country_id=country.id, resource_id=resource.id).first()
    if not stockpile:
        # Create a new stockpile
        stockpile = Stockpile(country_id=country.id, resource_id=resource.id, quantity=0)
        session.add(stockpile)
        session.flush()
    stockpile.quantity += extracted_quantity
    print(f"Extracted {extracted_quantity} of '{resource.name}' and added to {country.name}'s stockpile.")
