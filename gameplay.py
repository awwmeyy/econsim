# gameplay.py

import os
import json
from openai import OpenAI
from sqlalchemy.orm import Session
from models import (
    Game, Turn, Country, Industry, Action, Resource,
    StartNewIndustryAction, ExpandIndustryAction, UpgradeTechnologyAction, IndustryInput, IndustryOutput, TechnologyUpgrade
)
from sqlalchemy import and_

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def process_ai_turn(game: Game, turn_number: int, session: Session):
    """
    Processes the turn for all AI-controlled countries.

    Args:
        game (Game): The current game instance.
        turn_number (int): The current turn number.
        session (Session): The SQLAlchemy session.
    """
    countries = session.query(Country).filter_by(game_id=game.id, is_ai=True).all()
    if not countries:
        print("No AI-controlled countries found for the current game.")
        return

    for country in countries:
        print(f"Processing AI decisions for country: {country.name}")
        # Prepare the prompt for the AI
        prompt = prepare_ai_prompt(country, turn_number, session)

        # Get the AI's decision
        response_text = get_openai_response(prompt)

        # Parse the AI's response to get the selected action
        selected_action_data = parse_ai_response(response_text)

        # Apply the selected action to the game state
        if selected_action_data:
            apply_ai_action(country, turn_number, selected_action_data, session)
        else:
            print(f"Failed to process AI decision for country {country.name}.")

def prepare_ai_prompt(country: Country, turn_number: int, session: Session):
    """
    Prepares the prompt for the AI-controlled country using LLMTurn.md.

    Args:
        country (Country): The Country instance.
        turn_number (int): The current turn number.
        session (Session): The SQLAlchemy session.

    Returns:
        str: The prepared prompt.
    """
    # Read the LLMTurn.md prompt
    with open('prompts/gameplay/LLMTurn.md', 'r') as f:
        base_prompt = f.read()

    # Prepare the country schema
    country_schema = prepare_country_schema(country, session)
    country_schema_json = json.dumps(country_schema, indent=2)

    # Get the available actions for the country at this turn
    available_actions = get_available_actions(country, turn_number, session)
    available_actions_json = json.dumps(available_actions, indent=2)

    # Get the marketplace prices
    marketplace_data = get_marketplace_data(session)
    marketplace_data_json = json.dumps(marketplace_data, indent=2)

    # Prepare the final prompt
    prompt = f"{base_prompt}\n\n### **Current Turn Information**\nTurn Number: {turn_number}\n\n### **Country Schema**\n```json\n{country_schema_json}\n```\n\n### **Marketplace Prices**\n```json\n{marketplace_data_json}\n```\n\n### **Available Actions**\n```json\n{available_actions_json}\n```"

    return prompt

def get_available_actions(country: Country, turn_number: int, session: Session):
    """
    Retrieves the available actions for a country at a given turn.

    Args:
        country (Country): The Country instance.
        turn_number (int): The current turn number.
        session (Session): The SQLAlchemy session.

    Returns:
        dict: Dictionary containing lists of available actions.
    """
    actions = {
        "StartNewIndustry": [],
        "ExpandIndustry": [],
        "UpgradeTechnology": []
    }

    # Get the current turn
    turn = session.query(Turn).filter(
        and_(Turn.game_id == country.game_id, Turn.turn_number == turn_number)
    ).first()
    if not turn:
        return actions

    # Get StartNewIndustry actions
    new_industry_actions = session.query(StartNewIndustryAction).filter_by(
        turn_id=turn.id, country_id=country.id, selected=False
    ).all()
    for action in new_industry_actions:
        actions["StartNewIndustry"].append({
            "ActionID": action.id,
            "IndustryID": action.industry_id,
            "Type": action.industry_type,
            "SubType": action.sub_type,
            "SetupCost": action.setup_cost,
            "ProductionLevel": action.production_level,
            "TechnologyLevel": action.technology_level,
            "InputsRequired": json.loads(action.inputs_required),
            "OutputsProduced": json.loads(action.outputs_produced),
            "SkilledWorkersRequired": action.skilled_workers_required,
            "UnskilledWorkersRequired": action.unskilled_workers_required
        })

    # Get ExpandIndustry actions
    expand_actions = session.query(ExpandIndustryAction).filter_by(
        turn_id=turn.id, country_id=country.id, selected=False
    ).all()
    for action in expand_actions:
        actions["ExpandIndustry"].append({
            "ActionID": action.id,
            "IndustryID": action.industry_id,
            "NewProductionLevel": action.new_production_level,
            "ExpansionCost": action.expansion_cost,
            "AdditionalSkilledWorkersRequired": action.additional_skilled_workers_required,
            "AdditionalUnskilledWorkersRequired": action.additional_unskilled_workers_required,
            "IncreaseInOutputs": json.loads(action.increase_in_outputs),
            "AdditionalInputsRequired": json.loads(action.additional_inputs_required)
        })

    # Get UpgradeTechnology actions
    upgrade_actions = session.query(UpgradeTechnologyAction).filter_by(
        turn_id=turn.id, country_id=country.id, selected=False
    ).all()
    for action in upgrade_actions:
        actions["UpgradeTechnology"].append({
            "ActionID": action.id,
            "IndustryID": action.industry_id,
            "NewTechnologyLevel": action.new_technology_level,
            "UpgradeCost": action.upgrade_cost,
            "TimeToComplete": action.time_to_complete,
            "Benefits": action.benefits
        })

    return actions

def get_marketplace_data(session: Session):
    """
    Retrieves the current marketplace prices.

    Args:
        session (Session): The SQLAlchemy session.

    Returns:
        dict: Marketplace prices data.
    """
    resources = session.query(Resource).all()
    marketplace = {}
    for resource in resources:
        marketplace[resource.name] = {
            "CurrentPrice": float(resource.current_price),
            "QuantityThreshold": resource.quantity_threshold,
            "MaxTransactionPerTurn": resource.max_transaction_per_turn,
            "MaxPrice": float(resource.max_price),
            "MinPrice": float(resource.min_price)
        }
    return {"Marketplace": marketplace}

def parse_ai_response(response_text):
    """
    Parses the AI's response to get the selected action.

    Args:
        response_text (str): The response text from OpenAI.

    Returns:
        dict: The selected action data.
    """
    try:
        # Remove code fences if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove ```
        response_text = response_text.strip()

        # Parse JSON
        ai_response = json.loads(response_text)

        return ai_response.get("Actions", [])[0]  # Get the first (and only) action
    except json.JSONDecodeError as e:
        print("Failed to parse AI response JSON.")
        print("Response text:", response_text)
        print("Error message:", str(e))
        return None

def apply_ai_action(country: Country, turn_number: int, action_data, session: Session):
    """
    Applies the AI-selected action to the game state.

    Args:
        country (Country): The Country instance.
        turn_number (int): The current turn number.
        action_data (dict): The selected action data.
        session (Session): The SQLAlchemy session.
    """
    try:
        action_type = action_data.get("ActionType")
        action_id = action_data.get("ActionID")
        # Mark the action as selected
        base_action = session.query(Action).filter_by(
            id=action_id,
            country_id=country.id
        ).first()
        if not base_action:
            print(f"Action ID {action_id} not found for country {country.name}.")
            return

        if base_action.selected:
            print(f"Action ID {action_id} has already been selected.")
            return

        base_action.selected = True

        if action_type == "StartNewIndustry":
            apply_start_new_industry_action(base_action, country, session)
        elif action_type == "ExpandIndustry":
            apply_expand_industry_action(base_action, country, session)
        elif action_type == "UpgradeTechnology":
            apply_upgrade_technology_action(base_action, country, session)
        else:
            print(f"Unknown action type: {action_type}")
            return

        session.commit()
        print(f"Applied action {action_type} for country {country.name}.")

    except Exception as e:
        session.rollback()
        print(f"Error applying action for country {country.name}: {e}")

def apply_start_new_industry_action(action: StartNewIndustryAction, country: Country, session: Session):
    """
    Applies a StartNewIndustryAction to the game state.

    Args:
        action (StartNewIndustryAction): The action to apply.
        country (Country): The Country instance.
        session (Session): The SQLAlchemy session.
    """
    # Deduct setup cost from government's capital pool
    country.government_capital -= action.setup_cost

    # Deduct workers from unemployed workforce
    country.unemployed_skilled_workers -= action.skilled_workers_required
    country.unemployed_unskilled_workers -= action.unskilled_workers_required

    # Create the new industry
    industry = Industry(
        country_id=country.id,
        industry_id=action.industry_id,
        type=action.industry_type,
        sub_type=action.sub_type,
        production_level=action.production_level,
        technology_level=action.technology_level,
        skilled_workers_employed=action.skilled_workers_required,
        unskilled_workers_employed=action.unskilled_workers_required
    )
    session.add(industry)
    session.flush()

    # Add Industry Inputs
    inputs_required = json.loads(action.inputs_required)
    for resource_name, quantity in inputs_required.items():
        resource = get_or_create_resource(resource_name, session)
        industry_input = IndustryInput(
            industry_id=industry.id,
            resource_id=resource.id,
            quantity=quantity,
        )
        session.add(industry_input)

    # Add Industry Outputs
    outputs_produced = json.loads(action.outputs_produced)
    for resource_name, quantity in outputs_produced.items():
        resource = get_or_create_resource(resource_name, session)
        industry_output = IndustryOutput(
            industry_id=industry.id,
            resource_id=resource.id,
            quantity=quantity,
        )
        session.add(industry_output)

def apply_expand_industry_action(action: ExpandIndustryAction, country: Country, session: Session):
    """
    Applies an ExpandIndustryAction to the game state.

    Args:
        action (ExpandIndustryAction): The action to apply.
        country (Country): The Country instance.
        session (Session): The SQLAlchemy session.
    """
    # Deduct expansion cost from government's capital pool
    country.government_capital -= action.expansion_cost

    # Deduct additional workers from unemployed workforce
    country.unemployed_skilled_workers -= action.additional_skilled_workers_required
    country.unemployed_unskilled_workers -= action.additional_unskilled_workers_required

    # Update the industry's production level and workforce
    industry = session.query(Industry).filter_by(id=action.industry_id).first()
    industry.production_level = action.new_production_level
    industry.skilled_workers_employed += action.additional_skilled_workers_required
    industry.unskilled_workers_employed += action.additional_unskilled_workers_required

    # Update industry inputs and outputs if necessary
    # For simplicity, we can assume inputs and outputs scale with production level

def apply_upgrade_technology_action(action: UpgradeTechnologyAction, country: Country, session: Session):
    """
    Applies an UpgradeTechnologyAction to the game state.

    Args:
        action (UpgradeTechnologyAction): The action to apply.
        country (Country): The Country instance.
        session (Session): The SQLAlchemy session.
    """
    # Deduct upgrade cost from government's capital pool
    country.government_capital -= action.upgrade_cost

    # Create a TechnologyUpgrade record
    tech_upgrade = TechnologyUpgrade(
        industry_id=action.industry_id,
        initiated_turn_id=action.turn_id,
        new_technology_level=action.new_technology_level,
        upgrade_cost=action.upgrade_cost,
        total_time_required=action.time_to_complete,
        remaining_time=action.time_to_complete,
        benefits=action.benefits,
        is_completed=False
    )
    session.add(tech_upgrade)

# helpers (dup code, refactor later aaaaaaa)

def get_or_create_resource(resource_name, session: Session):
    """
    Gets a Resource by name, or creates it if it doesn't exist.

    Args:
        resource_name (str): The name of the resource.
        session (Session): The SQLAlchemy session.

    Returns:
        Resource: The Resource instance.
    """
    resource = session.query(Resource).filter_by(name=resource_name).first()
    if not resource:
        # Create a new Resource with default values
        resource = Resource(
            name=resource_name,
            base_price=0,  # Placeholder, to be set later
            current_price=0,  # Placeholder, to be set later
            quantity_threshold=0,  # Placeholder, to be set later
            max_transaction_per_turn=0,  # Placeholder, to be set later
            max_price=0,  # Placeholder, to be set later
            min_price=0,  # Placeholder, to be set later
        )
        session.add(resource)
        session.flush()  # Get resource.id
    return resource

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
        response_text = response.choices[0].message.content
        return response_text
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return ""

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