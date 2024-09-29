# background_logic.py

import json
from sqlalchemy.orm import Session
from models import (
    Game, Country, Industry, Stockpile, NaturalResource,
    TechnologyUpgrade, IndustryExpansion, IndustryInput, IndustryOutput, Resource
)
from sqlalchemy import and_

def process_background_logic(game: Game, session: Session, turn_number: int):
    """
    Processes the background logic for each turn:
    - Processes technology upgrades
    - Processes industry expansions
    - Consumes industry inputs and produces outputs
    - Extracts natural resources
    """
    countries = session.query(Country).filter_by(game_id=game.id).all()
    if not countries:
        print("No countries found for the current game.")
        return

    print(f"Processing background logic for Turn {turn_number}...")

    for country in countries:
        print(f"\nProcessing country: {country.name}")

        # Process technology upgrades
        process_technology_upgrades(country, session)

        # Process industry expansions
        process_industry_expansions(country, session)

        # Process industries
        for industry in country.industries:
            process_industry(industry, country, session)

        # Extract natural resources
        for nat_resource in country.natural_resources:
            extract_natural_resource(nat_resource, country, session)

    # Commit the session after processing all countries
    session.commit()
    print(f"\nBackground logic for Turn {turn_number} has been completed.\n")


def process_technology_upgrades(country: Country, session: Session):
    """
    Processes pending technology upgrades for a country's industries.
    """
    for industry in country.industries:
        for upgrade in industry.technology_upgrades:
            if not upgrade.is_completed:
                upgrade.remaining_time -= 1
                if upgrade.remaining_time <= 0:
                    # Upgrade complete
                    industry.technology_level = upgrade.new_technology_level
                    upgrade.is_completed = True

                    # Apply benefits as per 'benefits' field
                    # 'benefits' is expected to be a JSON string, parse it
                    benefits = json.loads(upgrade.benefits)

                    # Adjust industry attributes as per benefits
                    apply_technology_upgrade_benefits(industry, benefits, country, session)

                    # Update the database
                    session.add(industry)
                    session.add(upgrade)
                    session.commit()

                    print(f"Technology upgrade completed for industry '{industry.sub_type}' in {country.name}. New technology level: {industry.technology_level}")
                else:
                    session.add(upgrade)  # To track the decremented remaining_time
                    session.commit()
                    print(f"Technology upgrade in progress for industry '{industry.sub_type}' in {country.name}. Remaining time: {upgrade.remaining_time}")

def apply_technology_upgrade_benefits(industry: Industry, benefits: dict, country: Country, session: Session):
    """
    Applies the benefits of a technology upgrade to an industry.
    """
    # Retrieve benefit percentages
    unskilled_reduction_percent = benefits.get('Unskilled Labor Reduction', 0)
    skilled_reduction_percent = benefits.get('Skilled Labor Reduction', 0)
    output_increase_percent = benefits.get('Output Increase', 0)
    input_decrease_percent = benefits.get('Input Decrease', 0)

    # Adjust labor requirements
    previous_unskilled_workers = industry.unskilled_workers_employed
    previous_skilled_workers = industry.skilled_workers_employed

    unskilled_workers_reduced = int(previous_unskilled_workers * unskilled_reduction_percent / 100)
    skilled_workers_reduced = int(previous_skilled_workers * skilled_reduction_percent / 100)

    industry.unskilled_workers_employed -= unskilled_workers_reduced
    industry.skilled_workers_employed -= skilled_workers_reduced

    # Return workers to country's unemployed workforce
    country.unemployed_unskilled_workers += unskilled_workers_reduced
    country.unemployed_skilled_workers += skilled_workers_reduced

    # Update the database
    session.add(country)
    session.add(industry)

    print(f"Adjusted labor requirements for industry '{industry.sub_type}':")
    print(f" - Unskilled Workers Reduced by {unskilled_workers_reduced}, now employed: {industry.unskilled_workers_employed}")
    print(f" - Skilled Workers Reduced by {skilled_workers_reduced}, now employed: {industry.skilled_workers_employed}")

    # Adjust inputs
    if input_decrease_percent > 0:
        for industry_input in industry.inputs:
            original_quantity = industry_input.quantity
            reduced_quantity = original_quantity * (1 - input_decrease_percent / 100)
            industry_input.quantity = max(reduced_quantity, 0)  # Ensure non-negative
            session.add(industry_input)  # Update the database
            print(f"Reduced input '{industry_input.resource.name}' from {original_quantity} to {industry_input.quantity} per production cycle.")

    # Adjust outputs
    if output_increase_percent > 0:
        for industry_output in industry.outputs:
            original_quantity = industry_output.quantity
            increased_quantity = original_quantity * (1 + output_increase_percent / 100)
            industry_output.quantity = max(increased_quantity, 0)  # Ensure non-negative
            session.add(industry_output)  # Update the database
            print(f"Increased output '{industry_output.resource.name}' from {original_quantity} to {industry_output.quantity} per production cycle.")


def process_industry_expansions(country: Country, session: Session):
    """
    Processes pending industry expansions for a country's industries.
    """
    for industry in country.industries:
        for expansion in industry.expansions:
            if not expansion.is_completed:
                expansion.remaining_time -= 1
                if expansion.remaining_time <= 0:
                    # Expansion complete
                    industry.production_level = expansion.new_production_level
                    expansion.is_completed = True

                    # Apply benefits as per 'increase_in_outputs' and 'additional_inputs_required'
                    apply_expansion_benefits(industry, expansion, session)

                    # Update the database
                    session.add(industry)
                    session.add(expansion)
                    session.commit()

                    print(f"Industry expansion completed for '{industry.sub_type}' in {country.name}. New production level: {industry.production_level}")
                else:
                    session.add(expansion)  # To track the decremented remaining_time
                    session.commit()
                    print(f"Industry expansion in progress for '{industry.sub_type}' in {country.name}. Remaining time: {expansion.remaining_time}")

def apply_expansion_benefits(industry: Industry, expansion: IndustryExpansion, session: Session):
    """
    Applies the benefits of an industry expansion to the industry.
    """
    # Process increase in outputs
    if expansion.increase_in_outputs:
        increase_in_outputs = json.loads(expansion.increase_in_outputs)
        for resource_name, quantity_increase in increase_in_outputs.items():
            # Find the corresponding IndustryOutput
            industry_output = session.query(IndustryOutput).join(Resource).filter(
                IndustryOutput.industry_id == industry.id,
                Resource.name == resource_name
            ).first()
            if industry_output:
                original_quantity = industry_output.quantity
                industry_output.quantity += quantity_increase
                session.add(industry_output)
                print(f"Increased output '{resource_name}' from {original_quantity} to {industry_output.quantity} per production cycle.")
            else:
                print(f"Adding new output '{resource_name}' with quantity {quantity_increase}.")
                # Resource must be retrieved or created
                resource = session.query(Resource).filter_by(name=resource_name).first()
                if not resource:
                    # Create the resource if it doesn't exist
                    resource = Resource(name=resource_name)
                    session.add(resource)
                    session.flush()
                # Create new IndustryOutput
                new_industry_output = IndustryOutput(
                    industry_id=industry.id,
                    resource_id=resource.id,
                    quantity=quantity_increase
                )
                session.add(new_industry_output)
                print(f"Added new output '{resource_name}' with quantity {quantity_increase}.")

    # Process additional inputs required
    if expansion.additional_inputs_required:
        additional_inputs = json.loads(expansion.additional_inputs_required)
        for resource_name, additional_quantity in additional_inputs.items():
            # Find the corresponding IndustryInput
            industry_input = session.query(IndustryInput).join(Resource).filter(
                IndustryInput.industry_id == industry.id,
                Resource.name == resource_name
            ).first()
            if industry_input:
                original_quantity = industry_input.quantity
                industry_input.quantity += additional_quantity
                session.add(industry_input)
                print(f"Increased input '{resource_name}' from {original_quantity} to {industry_input.quantity} per production cycle.")
            else:
                print(f"Adding new input '{resource_name}' with quantity {additional_quantity}.")
                # Resource must be retrieved or created
                resource = session.query(Resource).filter_by(name=resource_name).first()
                if not resource:
                    # Create the resource if it doesn't exist
                    resource = Resource(name=resource_name)
                    session.add(resource)
                    session.flush()
                # Create new IndustryInput
                new_industry_input = IndustryInput(
                    industry_id=industry.id,
                    resource_id=resource.id,
                    quantity=additional_quantity
                )
                session.add(new_industry_input)
                print(f"Added new input '{resource_name}' with quantity {additional_quantity}.")


def process_industry(industry: Industry, country: Country, session: Session):
    """
    Processes an industry for a country:
    - Consumes inputs
    - Produces outputs
    - Checks for sufficient inputs
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
            session.add(stockpile)
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
            session.add(stockpile)
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

    # Update the database
    session.add(nat_resource)
    session.add(stockpile)

    print(f"Extracted {extracted_quantity} of '{resource.name}' and added to {country.name}'s stockpile.")
