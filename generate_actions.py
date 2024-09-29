# gameplay.py

import os
import json
from openai import OpenAI
from sqlalchemy.orm import Session
from models import (
    Game, Turn, Country, Industry, Action,
    StartNewIndustryAction, ExpandIndustryAction, UpgradeTechnologyAction
)
from sqlalchemy import and_

# Get API Key from environment variable OPENROUTER_API_KEY
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_action_options_for_all_countries(game: Game, turn_number: int, session: Session):
    """
    Generates action options for all countries at the start of a turn.

    Args:
        game (Game): The current game instance.
        turn_number (int): The current turn number.
        session (Session): The SQLAlchemy session.
    """
    countries = session.query(Country).filter_by(game_id=game.id).all()
    if not countries:
        print("No countries found for the current game.")
        return

    print(f"Generating action options for Turn {turn_number}...")

    for country in countries:
        print(f"Processing country: {country.name}")
        # Generate options for new industries
        generate_new_industry_options(country, turn_number, session)
        # Generate options for expanding industries
        generate_expand_industry_options(country, turn_number, session)
        # Generate options for technology upgrades
        generate_tech_upgrade_options(country, turn_number, session)

    print(f"Action options for Turn {turn_number} have been generated.")

def generate_new_industry_options(country: Country, turn_number: int, session: Session):
    """
    Generates new industry options for a country.

    Args:
        country (Country): The country instance.
        turn_number (int): The current turn number.
        session (Session): The SQLAlchemy session.
    """
    # Get the country's schema
    country_schema = prepare_country_schema(country, session)

    # Read the prompt for generating new industries
    with open('prompts/gameplay/generateNewIndustries.md', 'r') as f:
        base_prompt = f.read()

    # Prepare the prompt by inserting the country schema
    country_schema_json = json.dumps(country_schema, indent=2)
    prompt = f"{base_prompt}\n\n---\n\n**Country Schema:**\n\n```json\n{country_schema_json}\n```"

    # Get the OpenAI API response
    response_text = get_openai_response(prompt)

    # Parse the JSON response
    new_industries_data = parse_action_response(response_text, key='NewIndustries')

    # Store the actions in the database
    if new_industries_data:
        store_new_industry_actions(country, turn_number, new_industries_data, session)
    else:
        print(f"Failed to generate new industry options for {country.name}.")

def generate_expand_industry_options(country: Country, turn_number: int, session: Session):
    """
    Generates expand industry options for a country.

    Args:
        country (Country): The country instance.
        turn_number (int): The current turn number.
        session (Session): The SQLAlchemy session.
    """
    # Get the country's schema
    country_schema = prepare_country_schema(country, session)

    # Read the prompt for generating expand options
    with open('prompts/gameplay/generateExpandOptions.md', 'r') as f:
        base_prompt = f.read()

    # Prepare the prompt by inserting the country schema
    country_schema_json = json.dumps(country_schema, indent=2)
    prompt = f"{base_prompt}\n\n---\n\n**Country Schema:**\n\n```json\n{country_schema_json}\n```"

    # Get the OpenAI API response
    response_text = get_openai_response(prompt)

    # Parse the JSON response
    expand_options_data = parse_action_response(response_text, key='IndustryExpansions')

    # Store the actions in the database
    if expand_options_data:
        store_expand_industry_actions(country, turn_number, expand_options_data, session)
    else:
        print(f"Failed to generate expand industry options for {country.name}.")

def generate_tech_upgrade_options(country: Country, turn_number: int, session: Session):
    """
    Generates technology upgrade options for a country.

    Args:
        country (Country): The country instance.
        turn_number (int): The current turn number.
        session (Session): The SQLAlchemy session.
    """
    # Get the country's schema
    country_schema = prepare_country_schema(country, session)

    # Read the prompt for generating tech upgrade options
    with open('prompts/gameplay/generateTechUpgradeOptions.md', 'r') as f:
        base_prompt = f.read()

    # Prepare the prompt by inserting the country schema
    country_schema_json = json.dumps(country_schema, indent=2)
    prompt = f"{base_prompt}\n\n---\n\n**Country Schema:**\n\n```json\n{country_schema_json}\n```"

    # Get the OpenAI API response
    response_text = get_openai_response(prompt)

    # Parse the JSON response
    tech_upgrade_data = parse_action_response(response_text, key='TechnologyUpgrades')

    # Store the actions in the database
    if tech_upgrade_data:
        store_tech_upgrade_actions(country, turn_number, tech_upgrade_data, session)
    else:
        print(f"Failed to generate technology upgrade options for {country.name}.")

def get_openai_response(prompt):
    """
    Sends the prompt to the OpenAI API and returns the response text.

    Args:
        prompt (str): The prompt to send.

    Returns:
        str: The response text from OpenAI.
    """
    try:
        # Send the prompt to OpenAI API
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        response_text = response.choices[0].message.content.strip()
        return response_text
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return ""

def parse_action_response(response_text, key):
    """
    Parses the JSON response from OpenAI into a Python list.

    Args:
        response_text (str): The response text from OpenAI.
        key (str): The key in the JSON response to extract (e.g., 'NewIndustries').

    Returns:
        list: Parsed action data if successful, None otherwise.
    """
    try:
        # Remove code fences if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove ```
        response_text = response_text.strip()

        # Parse JSON
        action_data = json.loads(response_text)

        return action_data.get(key, [])
    except json.JSONDecodeError as e:
        print("Failed to parse JSON response.")
        print("Response text:", response_text)
        print("Error message:", str(e))
        return None

def store_new_industry_actions(country: Country, turn_number: int, new_industries_data, session: Session):
    """
    Stores StartNewIndustryAction instances in the database.

    Args:
        country (Country): The Country instance.
        turn_number (int): The current turn number.
        new_industries_data (list): List of new industry options.
        session (Session): The SQLAlchemy session.
    """
    try:
        # Get the current turn
        turn = session.query(Turn).filter(
            and_(Turn.game_id == country.game_id, Turn.turn_number == turn_number)
        ).first()
        if not turn:
            # Create a new Turn if it doesn't exist
            turn = Turn(
                game_id=country.game_id,
                turn_number=turn_number
            )
            session.add(turn)
            session.flush()

        for industry_option in new_industries_data:
            action = StartNewIndustryAction(
                turn_id=turn.id,
                country_id=country.id,
                selected=False,  # By default, not selected
                industry_id=industry_option.get('Industry ID'),
                industry_type=industry_option.get('Type'),
                sub_type=industry_option.get('Sub-Type'),
                setup_cost=industry_option.get('Setup Cost'),
                production_level=industry_option.get('Production Level'),
                technology_level=industry_option.get('Technology Level'),
                inputs_required=json.dumps(industry_option.get('Inputs Required', {})),
                outputs_produced=json.dumps(industry_option.get('Outputs Produced', {})),
                skilled_workers_required=industry_option.get('Skilled Workers Required'),
                unskilled_workers_required=industry_option.get('Unskilled Workers Required'),
            )
            session.add(action)

        session.commit()
        print(f"Stored {len(new_industries_data)} new industry options for country {country.name}.")

    except Exception as e:
        session.rollback()
        print(f"Error storing new industry actions for {country.name}: {e}")

def store_expand_industry_actions(country: Country, turn_number: int, expand_options_data, session: Session):
    """
    Stores ExpandIndustryAction instances in the database.

    Args:
        country (Country): The Country instance.
        turn_number (int): The current turn number.
        expand_options_data (list): List of expand industry options.
        session (Session): The SQLAlchemy session.
    """
    try:
        # Get the current turn
        turn = session.query(Turn).filter(
            and_(Turn.game_id == country.game_id, Turn.turn_number == turn_number)
        ).first()
        if not turn:
            # Create a new Turn if it doesn't exist
            turn = Turn(
                game_id=country.game_id,
                turn_number=turn_number
            )
            session.add(turn)
            session.flush()

        for expand_option in expand_options_data:
            # Get the industry
            industry = session.query(Industry).filter_by(
                country_id=country.id,
                industry_id=expand_option.get('Industry ID')
            ).first()
            if not industry:
                print(f"Industry {expand_option.get('Industry ID')} not found for country {country.name}.")
                continue

            action = ExpandIndustryAction(
                turn_id=turn.id,
                country_id=country.id,
                selected=False,
                industry_id=industry.id,
                new_production_level=expand_option.get('New Production Level'),
                expansion_cost=expand_option.get('Expansion Cost'),
                additional_skilled_workers_required=expand_option.get('Additional Skilled Workers Required'),
                additional_unskilled_workers_required=expand_option.get('Additional Unskilled Workers Required'),
                increase_in_outputs=json.dumps(expand_option.get('Increase in Outputs', {})),
                additional_inputs_required=json.dumps(expand_option.get('Additional Inputs Required', {})),
            )
            session.add(action)

        session.commit()
        print(f"Stored {len(expand_options_data)} expand industry options for country {country.name}.")

    except Exception as e:
        session.rollback()
        print(f"Error storing expand industry actions for {country.name}: {e}")

def store_tech_upgrade_actions(country: Country, turn_number: int, tech_upgrade_data, session: Session):
    """
    Stores UpgradeTechnologyAction instances in the database.

    Args:
        country (Country): The Country instance.
        turn_number (int): The current turn number.
        tech_upgrade_data (list): List of tech upgrade options.
        session (Session): The SQLAlchemy session.
    """
    try:
        # Get the current turn
        turn = session.query(Turn).filter(
            and_(Turn.game_id == country.game_id, Turn.turn_number == turn_number)
        ).first()
        if not turn:
            # Create a new Turn if it doesn't exist
            turn = Turn(
                game_id=country.game_id,
                turn_number=turn_number
            )
            session.add(turn)
            session.flush()

        for upgrade_option in tech_upgrade_data:
            # Get the industry
            industry = session.query(Industry).filter_by(
                country_id=country.id,
                industry_id=upgrade_option.get('Industry ID')
            ).first()
            if not industry:
                print(f"Industry {upgrade_option.get('Industry ID')} not found for country {country.name}.")
                continue

            action = UpgradeTechnologyAction(
                turn_id=turn.id,
                country_id=country.id,
                selected=False,
                industry_id=industry.id,
                new_technology_level=upgrade_option.get('New Technology Level'),
                upgrade_cost=upgrade_option.get('Upgrade Cost'),
                time_to_complete=upgrade_option.get('Time to Complete'),
                benefits=upgrade_option.get('Benefits'),
            )
            session.add(action)

        session.commit()
        print(f"Stored {len(tech_upgrade_data)} technology upgrade options for country {country.name}.")

    except Exception as e:
        session.rollback()
        print(f"Error storing technology upgrade actions for {country.name}: {e}")


# HELPER FUNCTION

def prepare_country_schema(country: Country, session: Session):
    """
    Prepares the country schema as a dictionary for the prompt.

    Args:
        country (Country): The Country instance.
        session (Session): The SQLAlchemy session.

    Returns:
        dict: The country schema.
    """
    # Industries
    industries = []
    for industry in country.industries:
        # Inputs
        inputs = {}
        for industry_input in industry.inputs:
            resource_name = industry_input.resource.name
            quantity = industry_input.quantity
            inputs[resource_name] = quantity

        # Outputs
        outputs = {}
        for industry_output in industry.outputs:
            resource_name = industry_output.resource.name
            quantity = industry_output.quantity
            outputs[resource_name] = quantity

        industry_data = {
            "Industry ID": industry.industry_id,
            "Type": industry.type,
            "Sub-Type": industry.sub_type,
            "Production Level": industry.production_level,
            "Technology Level": industry.technology_level,
            "Inputs": inputs,
            "Outputs": outputs,
            "Skilled Workers Employed": industry.skilled_workers_employed,
            "Unskilled Workers Employed": industry.unskilled_workers_employed
        }
        industries.append(industry_data)

    # Workforce
    workforce = {
        "Unemployed Skilled Workers": country.unemployed_skilled_workers,
        "Unemployed Unskilled Workers": country.unemployed_unskilled_workers
    }

    # Stockpiles
    stockpiles = {}
    for stockpile in country.stockpiles:
        resource_name = stockpile.resource.name
        quantity = stockpile.quantity
        stockpiles[resource_name] = quantity

    # Natural Resources
    natural_resources = {}
    for nat_resource in country.natural_resources:
        resource_name = nat_resource.resource.name
        resource_info = {
            "Total Reserves": nat_resource.total_reserves,
            "Extraction Rate": nat_resource.extraction_rate
        }
        natural_resources[resource_name] = resource_info

    # Country schema
    country_schema = {
        "Country Name": country.name,
        "Government Capital Pool": float(country.government_capital),
        "Industries": industries,
        "Workforce": workforce,
        "Stockpiles": stockpiles,
        "Natural Resources": natural_resources
    }

    return country_schema

