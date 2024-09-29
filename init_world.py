# init_world.py

import os
import json
from openai import OpenAI
from sqlalchemy.orm import Session
from models import Country, Industry, IndustryInput, IndustryOutput, Stockpile, NaturalResource, Resource

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)


def generate_initial_world(game, num_players, session: Session):
    """
    Generates the initial game world by creating countries for AI players.

    Args:
        game (Game): The current game instance.
        num_players (int): Number of AI players.
        session (Session): The SQLAlchemy session.
    """
    # List to keep track of existing countries' data
    existing_countries = []

    for i in range(num_players):
        print(f"Generating country {i+1}/{num_players}...")
        # Generate country data using OpenAI API
        country_data = generate_country(existing_countries)
        if country_data:
            # Add the country to the database
            add_country_to_db(country_data, game.id, session)
            # Append the country's schema to existing_countries
            existing_countries.append(country_data)
        else:
            print(f"Failed to generate country {i+1}.")

    print("All AI countries have been generated.")

def generate_country(existing_countries):
    """
    Generates a country's data using the OpenAI API.

    Args:
        existing_countries (list): List of existing countries' data.

    Returns:
        dict: Parsed country data if successful, None otherwise.
    """
    # Prepare the prompt
    prompt = generate_prompt(existing_countries)

    # Get the OpenAI API response
    response_text = get_openai_response(prompt)

    # Parse the JSON response
    country_data = parse_country_response(response_text)

    return country_data

def generate_prompt(existing_countries):
    """
    Generates the prompt for the OpenAI API, including existing countries.

    Args:
        existing_countries (list): List of existing countries' data.

    Returns:
        str: The prepared prompt.
    """
    # Read the contents of generatePlayers.md
    with open('prompts/initialize/generatePlayers.md', 'r') as f:
        base_prompt = f.read()

    # Include existing countries in the prompt if any
    if existing_countries:
        existing_countries_json = json.dumps(existing_countries, indent=2)
        prompt = f"{base_prompt}\n\nExisting Countries:\n{existing_countries_json}"
    else:
        prompt = base_prompt

    return prompt

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

def parse_country_response(response_text):
    """
    Parses the JSON response from OpenAI into a Python dictionary.

    Args:
        response_text (str): The response text from OpenAI.

    Returns:
        dict: Parsed country data if successful, None otherwise.
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
        country_data = json.loads(response_text)
        return country_data
    except json.JSONDecodeError as e:
        print("Failed to parse JSON response.")
        print("Response text:", response_text)
        print("Error message:", str(e))
        return None

def add_country_to_db(country_data, game_id, session: Session):
    """
    Maps the country data to SQLAlchemy models and inserts them into the database.

    Args:
        country_data (dict): The country data to insert.
        game_id (int): The ID of the current game.
        session (Session): The SQLAlchemy session.
    """
    try:
        # Create Country instance
        country = Country(
            game_id=game_id,
            name=country_data["Country Name"],
            is_ai=True,
            government_capital=country_data["Government Capital Pool"],
            # Workforce details
            total_skilled_workers=(
                country_data["Workforce"]["Unemployed Skilled Workers"] +
                sum(industry["Skilled Workers Employed"] for industry in country_data["Industries"])
            ),
            total_unskilled_workers=(
                country_data["Workforce"]["Unemployed Unskilled Workers"] +
                sum(industry["Unskilled Workers Employed"] for industry in country_data["Industries"])
            ),
            unemployed_skilled_workers=country_data["Workforce"]["Unemployed Skilled Workers"],
            unemployed_unskilled_workers=country_data["Workforce"]["Unemployed Unskilled Workers"],
        )
        session.add(country)
        session.flush()  # Get country.id

        # Add Industries
        for industry_data in country_data["Industries"]:
            industry = Industry(
                country_id=country.id,
                industry_id=industry_data["Industry ID"],
                type=industry_data["Type"],
                sub_type=industry_data["Sub-Type"],
                production_level=industry_data["Production Level"],
                technology_level=industry_data["Technology Level"],
                skilled_workers_employed=industry_data["Skilled Workers Employed"],
                unskilled_workers_employed=industry_data["Unskilled Workers Employed"],
            )
            session.add(industry)
            session.flush()  # Get industry.id

            # Add Industry Inputs
            for resource_name, quantity in industry_data.get("Inputs", {}).items():
                resource = get_or_create_resource(resource_name, session)
                industry_input = IndustryInput(
                    industry_id=industry.id,
                    resource_id=resource.id,
                    quantity=quantity,
                )
                session.add(industry_input)

            # Add Industry Outputs
            for resource_name, quantity in industry_data.get("Outputs", {}).items():
                resource = get_or_create_resource(resource_name, session)
                industry_output = IndustryOutput(
                    industry_id=industry.id,
                    resource_id=resource.id,
                    quantity=quantity,
                )
                session.add(industry_output)

        # Add Stockpiles
        for resource_name, quantity in country_data.get("Stockpiles", {}).items():
            resource = get_or_create_resource(resource_name, session)
            stockpile = Stockpile(
                country_id=country.id,
                resource_id=resource.id,
                quantity=quantity,
            )
            session.add(stockpile)

        # Add Natural Resources
        for resource_name, resource_info in country_data.get("Natural Resources", {}).items():
            resource = get_or_create_resource(resource_name, session)
            natural_resource = NaturalResource(
                country_id=country.id,
                resource_id=resource.id,
                total_reserves=resource_info["Total Reserves"],
                extraction_rate=resource_info["Extraction Rate"],
            )
            session.add(natural_resource)

        session.commit()
        print(f"Country '{country.name}' added to the database.")

    except Exception as e:
        session.rollback()
        print(f"Error adding country to the database: {e}")

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
