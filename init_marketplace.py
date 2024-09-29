# init_marketplace.py

import os
import json
from openai import OpenAI
from sqlalchemy.orm import Session
from models import Country, Resource

# Gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_marketplace_data(game_id, session: Session):
    """
    Generates the initial marketplace data by sending a prompt to the OpenAI API
    and updating the Resource table with the response.

    Args:
        game_id (int): The ID of the current game.
        session (Session): The SQLAlchemy session.
    """
    print("Generating marketplace data...")
    # Fetch all countries in the game
    countries = session.query(Country).filter_by(game_id=game_id).all()
    if not countries:
        print("No countries found for the given game ID.")
        return

    # Generate the prompt
    prompt = generate_prompt(countries, session)

    # Get the OpenAI API response
    response_text = get_openai_response(prompt)

    # Parse the JSON response
    marketplace_data = parse_marketplace_response(response_text)
    if marketplace_data:
        # Update the database with the marketplace data
        update_resources_in_db(marketplace_data, session)
    else:
        print("Failed to generate marketplace data.")

    print("Marketplace data generated successfully")


def generate_prompt(countries, session: Session):
    """
    Generates the prompt for the OpenAI API, including country schemas.

    Args:
        countries (list): List of Country instances.
        session (Session): The SQLAlchemy session.

    Returns:
        str: The prepared prompt.
    """
    # Read the contents of initializeMarketplace.md
    with open('prompts/initialize/initializeMarketplace.md', 'r') as f:
        base_prompt = f.read()

    # Prepare the country schemas
    country_schemas = []
    for country in countries:
        schema = prepare_country_schema(country, session)
        country_schemas.append(schema)

    # Convert country_schemas to JSON string
    country_schemas_json = json.dumps(country_schemas, indent=2)

    # Insert the country schemas into the prompt
    prompt = f"{base_prompt}\n\n### **Country Schemas:**\n\n{country_schemas_json}"

    return prompt


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
            model="anthropic/claude-3.5-sonnet",
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


def parse_marketplace_response(response_text):
    """
    Parses the JSON response from OpenAI into a Python dictionary.

    Args:
        response_text (str): The response text from OpenAI.

    Returns:
        dict: Parsed marketplace data if successful, None otherwise.
    """
    # The response is expected to be in JSON format within code fences
    try:
        # Remove code fences if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove ```
        response_text = response_text.strip()

        # Parse JSON
        marketplace_data = json.loads(response_text)
        return marketplace_data
    except json.JSONDecodeError as e:
        print("Failed to parse JSON response.")
        print("Response text:", response_text)
        print("Error message:", str(e))
        return None


def update_resources_in_db(marketplace_data, session: Session):
    """
    Updates the Resource table with the marketplace data.

    Args:
        marketplace_data (dict): The marketplace data to insert.
        session (Session): The SQLAlchemy session.
    """
    try:
        resources_data = marketplace_data.get("Marketplace", {}).get("Resources", {})
        for resource_name, data in resources_data.items():
            # Get or create the resource
            resource = session.query(Resource).filter_by(name=resource_name).first()
            if not resource:
                # If resource does not exist, create it
                resource = Resource(
                    name=resource_name,
                    base_price=data["InitialPrice"],
                    current_price=data["InitialPrice"],
                    quantity_threshold=data["QuantityThreshold"],
                    max_transaction_per_turn=data["MaxTransactionPerTurn"],
                    max_price=data["MaxPrice"],
                    min_price=data["MinPrice"],
                )
                session.add(resource)
            else:
                # Update existing resource
                resource.base_price = data["InitialPrice"]
                resource.current_price = data["InitialPrice"]
                resource.quantity_threshold = data["QuantityThreshold"]
                resource.max_transaction_per_turn = data["MaxTransactionPerTurn"]
                resource.max_price = data["MaxPrice"]
                resource.min_price = data["MinPrice"]
                # No need to add to session, already tracked

        session.commit()
        print("Marketplace data has been updated in the database.")

    except Exception as e:
        session.rollback()
        print(f"Error updating marketplace data in the database: {e}")