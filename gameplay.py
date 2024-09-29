# gameplay.py

import os
import json
from openai import OpenAI
from sqlalchemy.orm import Session
from models import (
    Game, Turn, Country, Industry, Action, Resource, Stockpile,
    StartNewIndustryAction, ExpandIndustryAction, UpgradeTechnologyAction, IndustryInput, IndustryOutput, TechnologyUpgrade,
    MarketTransaction
)
from sqlalchemy import and_
from decimal import Decimal

# Define a custom exception for invalid actions
class InvalidActionException(Exception):
    pass

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def process_ai_turn(game: Game, turn_number: int, session: Session):
    """
    Processes the turn for all AI-controlled countries.
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

        # Parse the AI's response to get the actions list
        actions_data = parse_ai_response(response_text)

        # Apply each action to the game state
        if actions_data:
            try:
                for action_data in actions_data:
                    apply_ai_action(country, turn_number, action_data, session)
                print(f"Applied actions for country {country.name}.")
            except InvalidActionException as e:
                session.rollback()
                print(f"AI for country {country.name} made an invalid action: {e}")
                print(f"The turn is wasted, no actions were performed.")
        else:
            print(f"Failed to process AI decisions for country {country.name}.")

def prepare_ai_prompt(country: Country, turn_number: int, session: Session):
    """
    Prepares the prompt for the AI-controlled country using LLMTurn.md.
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
    prompt = f"{base_prompt}\n\n### **Current Turn Information**\nTurn Number: {turn_number}\n\n### **Country Schema**\n```json\n{country_schema_json}\n```\n\n### **Marketplace Prices**\n```json\n{marketplace_data_json}\n```\n\n### **Available Actions**\n```json\n{available_actions_json}\n```\n\n**Note: Options for BuySellResource actions are not pre-generated and should be decided based on the given data.**"

    return prompt

def get_available_actions(country: Country, turn_number: int, session: Session):
    """
    Retrieves the available actions for a country at a given turn.
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
            "SetupCost": float(action.setup_cost),
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
            "ExpansionCost": float(action.expansion_cost),
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
            "UpgradeCost": float(action.upgrade_cost),
            "TimeToComplete": action.time_to_complete,
            "Benefits": action.benefits
        })

    return actions

def get_marketplace_data(session: Session):
    """
    Retrieves the current marketplace prices.
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
    Parses the AI's response to get the actions.
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
        actions = ai_response.get("Actions", [])

        return actions
    except json.JSONDecodeError as e:
        print("Failed to parse AI response JSON.")
        print("Response text:", response_text)
        print("Error message:", str(e))
        return []

def apply_ai_action(country: Country, turn_number: int, action_data, session: Session):
    """
    Applies the AI-selected action to the game state.
    """
    action_type = action_data.get("ActionType")

    # For actions that require selection from pre-generated options
    if action_type in ["StartNewIndustry", "ExpandIndustry", "UpgradeTechnology"]:

        action_id = action_data.get("ActionID")

        # Map action types to their corresponding classes
        action_class_map = {
            "StartNewIndustry": StartNewIndustryAction,
            "ExpandIndustry": ExpandIndustryAction,
            "UpgradeTechnology": UpgradeTechnologyAction
        }

        action_class = action_class_map.get(action_type)
        if not action_class:
            raise InvalidActionException(f"Unknown action type: {action_type}.")

        # Fetch the action using the correct subclass
        base_action = session.query(action_class).filter_by(
            id=action_id,
            country_id=country.id
        ).first()

        if not base_action:
            raise InvalidActionException(f"Action ID {action_id} not found for country {country.name}.")

        if base_action.selected:
            raise InvalidActionException(f"Action ID {action_id} has already been selected.")

        base_action.selected = True
        session.add(base_action)
        session.commit()

        # Apply the action
        if action_type == "StartNewIndustry":
            apply_start_new_industry_action(base_action, country, session)
        elif action_type == "ExpandIndustry":
            apply_expand_industry_action(base_action, country, session)
        elif action_type == "UpgradeTechnology":
            apply_upgrade_technology_action(base_action, country, session)
        else:
            raise InvalidActionException(f"Unknown action type: {action_type}.")

    elif action_type == "BuySellResource":
        # Handle BuySellResource action directly from action_data
        apply_buy_sell_resource_action(action_data, country, turn_number, session)

    else:
        raise InvalidActionException(f"Unknown action type: {action_type}.")

    print(f"Applied action {action_type} for country {country.name}.")

def apply_start_new_industry_action(action: StartNewIndustryAction, country: Country, session: Session):
    """
    Applies a StartNewIndustryAction to the game state.
    """
    # Feasibility check
    # Convert setup_cost to Decimal for comparison
    setup_cost = Decimal(action.setup_cost)

    if country.government_capital < setup_cost:
        raise InvalidActionException(f"Not enough capital to start new industry (requires {setup_cost}, has {country.government_capital}).")

    # Check if country has enough workforce
    if country.unemployed_skilled_workers < action.skilled_workers_required:
        raise InvalidActionException(f"Not enough unemployed skilled workers to start new industry (requires {action.skilled_workers_required}, has {country.unemployed_skilled_workers}).")
    if country.unemployed_unskilled_workers < action.unskilled_workers_required:
        raise InvalidActionException(f"Not enough unemployed unskilled workers to start new industry (requires {action.unskilled_workers_required}, has {country.unemployed_unskilled_workers}).")

    # Deduct setup cost from government's capital pool
    country.government_capital -= setup_cost

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
    """
    # Feasibility check
    # Convert expansion_cost to Decimal for comparison
    expansion_cost = Decimal(action.expansion_cost)

    if country.government_capital < expansion_cost:
        raise InvalidActionException(f"Not enough capital to expand industry (requires {expansion_cost}, has {country.government_capital}).")

    # Check if country has enough workforce
    if country.unemployed_skilled_workers < action.additional_skilled_workers_required:
        raise InvalidActionException(f"Not enough unemployed skilled workers to expand industry (requires {action.additional_skilled_workers_required}, has {country.unemployed_skilled_workers}).")
    if country.unemployed_unskilled_workers < action.additional_unskilled_workers_required:
        raise InvalidActionException(f"Not enough unemployed unskilled workers to expand industry (requires {action.additional_unskilled_workers_required}, has {country.unemployed_unskilled_workers}).")

    # Deduct expansion cost from government's capital pool
    country.government_capital -= expansion_cost

    # Deduct additional workers from unemployed workforce
    country.unemployed_skilled_workers -= action.additional_skilled_workers_required
    country.unemployed_unskilled_workers -= action.additional_unskilled_workers_required

    # Update the industry's production level and workforce
    industry = session.query(Industry).filter_by(id=action.industry_id).first()
    industry.production_level = action.new_production_level
    industry.skilled_workers_employed += action.additional_skilled_workers_required
    industry.unskilled_workers_employed += action.additional_unskilled_workers_required

def apply_upgrade_technology_action(action: UpgradeTechnologyAction, country: Country, session: Session):
    """
    Applies an UpgradeTechnologyAction to the game state.
    """
    # Feasibility check
    # Convert upgrade_cost to Decimal for comparison
    upgrade_cost = Decimal(action.upgrade_cost)

    if country.government_capital < upgrade_cost:
        raise InvalidActionException(f"Not enough capital to upgrade technology (requires {upgrade_cost}, has {country.government_capital}).")

    # Deduct upgrade cost from government's capital pool
    country.government_capital -= upgrade_cost

    # Create a TechnologyUpgrade record
    tech_upgrade = TechnologyUpgrade(
        industry_id=action.industry_id,
        initiated_turn_id=action.turn_id,
        new_technology_level=action.new_technology_level,
        upgrade_cost=upgrade_cost,
        total_time_required=action.time_to_complete,
        remaining_time=action.time_to_complete,
        benefits=action.benefits,
        is_completed=False
    )
    session.add(tech_upgrade)

def apply_buy_sell_resource_action(action_data, country: Country, turn_number: int, session: Session):
    """
    Applies a BuySellResource action to the game state.
    """
    details = action_data.get("Details", {})
    transaction_type = details.get("TransactionType")
    resource_name = details.get("ResourceName")
    quantity = details.get("Quantity")
    total_price = details.get("TotalCost") or details.get("TotalRevenue")

    # Validate inputs
    if not all([transaction_type, resource_name, quantity, total_price]):
        raise InvalidActionException(f"Invalid BuySellResource action data for country {country.name}.")

    # Convert total_price to Decimal
    total_price = Decimal(str(total_price))

    # Get the resource
    resource = session.query(Resource).filter_by(name=resource_name).first()
    if not resource:
        raise InvalidActionException(f"Resource '{resource_name}' not found.")

    # Get or create the country's stockpile for the resource
    stockpile = session.query(Stockpile).filter_by(country_id=country.id, resource_id=resource.id).first()
    if not stockpile:
        if transaction_type == "Sell":
            raise InvalidActionException(f"Country '{country.name}' does not have any stockpile of '{resource_name}' to sell.")
        # If stockpile doesn't exist, create it with zero quantity for buying
        stockpile = Stockpile(country_id=country.id, resource_id=resource.id, quantity=0)
        session.add(stockpile)
        session.flush()  # To get stockpile.id

    max_transaction_per_turn = resource.max_transaction_per_turn

    if quantity > max_transaction_per_turn:
        raise InvalidActionException(f"Transaction quantity {quantity} exceeds MaxTransactionPerTurn for resource '{resource_name}'.")

    if transaction_type == "Buy":
        # Check if country has enough capital
        if country.government_capital < total_price:
            raise InvalidActionException(f"Country '{country.name}' does not have enough capital to buy {quantity} of '{resource_name}' (needs {total_price}, has {country.government_capital}).")

        # Update country's capital
        country.government_capital -= total_price

        # Update stockpile
        stockpile.quantity += quantity

        print(f"Country '{country.name}' bought {quantity} of '{resource_name}' for {total_price}.")

    elif transaction_type == "Sell":
        # Check if country has enough resource in stockpile
        if stockpile.quantity < quantity:
            raise InvalidActionException(f"Country '{country.name}' does not have enough '{resource_name}' to sell {quantity} (has {stockpile.quantity}).")

        # Update stockpile
        stockpile.quantity -= quantity

        # Update country's capital
        country.government_capital += total_price

        print(f"Country '{country.name}' sold {quantity} of '{resource_name}' for {total_price}.")

    else:
        raise InvalidActionException(f"Invalid TransactionType '{transaction_type}' for BuySellResource action.")

    # Record the transaction
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

    # Calculate price per unit as Decimal
    price_per_unit = total_price / Decimal(quantity)

    transaction = MarketTransaction(
        turn_id=turn.id,
        country_id=country.id,
        resource_id=resource.id,
        transaction_type=transaction_type,
        quantity=quantity,
        price_per_unit=price_per_unit,
        total_price=total_price
    )
    session.add(transaction)

    # Adjust the resource price after the transaction
    quantity_threshold = resource.quantity_threshold
    if quantity_threshold == 0:
        raise InvalidActionException(f"Resource '{resource_name}' has zero quantity_threshold.")

    # Calculate the percentage change proportionally using Decimal
    percentage_change = Decimal('0.05') * (Decimal(quantity) / Decimal(quantity_threshold))

    if transaction_type == "Buy":
        # Buying increases demand, price goes up
        new_price = resource.current_price * (Decimal('1') + percentage_change)
    elif transaction_type == "Sell":
        # Selling increases supply, price goes down
        new_price = resource.current_price * (Decimal('1') - percentage_change)
    else:
        raise InvalidActionException(f"Invalid TransactionType '{transaction_type}' for BuySellResource action.")

    # Ensure new price is within MinPrice and MaxPrice
    new_price = max(min(new_price, resource.max_price), resource.min_price)
    print(f"Adjusted price of '{resource_name}' from {resource.current_price} to {new_price} based on transaction of {quantity} units.")
    resource.current_price = new_price

def get_or_create_resource(resource_name, session: Session):
    """
    Gets a Resource by name, or creates it if it doesn't exist.
    """
    resource = session.query(Resource).filter_by(name=resource_name).first()
    if not resource:
        # Create a new Resource with default values
        resource = Resource(
            name=resource_name,
            base_price=Decimal('0.00'),  # Placeholder, to be set later
            current_price=Decimal('0.00'),  # Placeholder, to be set later
            quantity_threshold=0,  # Placeholder, to be set later
            max_transaction_per_turn=0,  # Placeholder, to be set later
            max_price=Decimal('0.00'),  # Placeholder, to be set later
            min_price=Decimal('0.00'),  # Placeholder, to be set later
        )
        session.add(resource)
        session.flush()  # Get resource.id
    return resource

def get_openai_response(prompt):
    """
    Sends the prompt to the OpenAI API and returns the response text.
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

def prepare_country_schema(country: Country, session: Session):
    """
    Prepares the country schema as a dictionary for the prompt.
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