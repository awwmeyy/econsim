# determine_winner.py

import os
import json
from openai import OpenAI
from sqlalchemy.orm import Session
from models import (
    Game, Country, Industry, IndustryInput, IndustryOutput, Stockpile, NaturalResource
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def pick_winner(game_id: int, session: Session):
    """
    Determines the winner of the game after 50 turns by evaluating the final states
    of all countries using an AI model as per the 'pickWinner.md' prompt.

    Args:
        game_id (int): The ID of the game to evaluate.
        session (Session): The SQLAlchemy session.

    Returns:
        dict: A dictionary containing the results and the winner.
    """
    try:
        # Fetch the game
        game = session.query(Game).filter_by(id=game_id).first()
        if not game:
            print(f"Game with ID {game_id} not found.")
            return

        # Ensure the game has completed 50 turns
        if game.current_turn_number < 50:
            print(f"Game has not completed 50 turns. Current turn: {game.current_turn_number}")
            return

        # Fetch all countries in the game
        countries = session.query(Country).filter_by(game_id=game_id).all()
        if not countries:
            print("No countries found for the given game ID.")
            return

        # Prepare the prompt
        prompt = prepare_winner_prompt(countries, session)

        # Send the prompt to the AI model
        ai_response_text = get_ai_response(prompt)

        # Parse the AI's response
        winner_data = parse_winner_response(ai_response_text)

        if winner_data:
            # Output the results
            output_json = json.dumps(winner_data, indent=2)
            print(output_json)
            return winner_data
        else:
            print("Failed to determine the winner.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def prepare_winner_prompt(countries, session: Session):
    """
    Prepares the prompt for the AI based on 'pickWinner.md', including the countries' data.

    Args:
        countries (list): List of Country instances.
        session (Session): The SQLAlchemy session.

    Returns:
        str: The prepared prompt.
    """
    # Read the contents of 'pickWinner.md' for the prompt
    with open('prompts/gameplay/pickWinner.md', 'r') as f:
        base_prompt = f.read()

    # Collect the end-state data for all countries
    country_data_list = []
    for country in countries:
        country_data = gather_country_end_state(country, session)
        country_data_list.append(country_data)

    # Convert the country data list to JSON string
    country_data_json = json.dumps(country_data_list, indent=2)

    # Prepare the final prompt by inserting the country data into the base prompt
    prompt = f"{base_prompt}\n\n### **End-State Data for All Countries:**\n```json\n{country_data_json}\n```\n\n**Remember:** Provide only the JSON output as specified, without additional commentary or text outside the structured format."

    return prompt

def gather_country_end_state(country: Country, session: Session):
    """
    Gathers the end-state data for a country after 50 turns.

    Args:
        country (Country): The Country instance.
        session (Session): The SQLAlchemy session.

    Returns:
        dict: A dictionary containing the country's end-state data.
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

    # Country data
    country_data = {
        "Country Name": country.name,
        "Government Capital Pool": float(country.government_capital),
        "Industries": industries,
        "Stockpiles": stockpiles,
        "Natural Resources": natural_resources
    }

    return country_data

def get_ai_response(prompt):
    """
    Sends the prompt to the AI model and returns the response text.

    Args:
        prompt (str): The prompt to send.

    Returns:
        str: The response text from the AI model.
    """
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4",
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

def parse_winner_response(response_text):
    """
    Parses the AI's response containing the winner and justifications.

    Args:
        response_text (str): The response text from the AI.

    Returns:
        dict: Parsed winner data if successful, None otherwise.
    """
    try:
        # Remove code fences if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove ```
        response_text = response_text.strip()

        # Parse JSON
        winner_data = json.loads(response_text)
        return winner_data
    except json.JSONDecodeError as e:
        print("Failed to parse AI response JSON.")
        print("Response text:", response_text)
        print("Error message:", str(e))
        return None
