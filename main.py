# main.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Game
from datetime import datetime
from init_world import generate_initial_world
from init_marketplace import generate_marketplace_data
from generate_actions import generate_action_options_for_all_countries
from gameplay import process_ai_turn
from pick_winner import pick_winner

# Database setup
DATABASE_URL = "sqlite:///game.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def main():
    session = SessionLocal()

    # Ask for username
    username = input("Enter your username: ").strip()

    # Check if user exists
    user = session.query(User).filter(User.username == username).first()

    if user:
        print(f"Welcome back, {username}!")
    else:
        # Create new user
        user = User(username=username)
        session.add(user)
        session.commit()
        print(f"New user created. Welcome, {username}!")

    # Ask if user wants to start a new game
    start_game = input("Do you want to start a new game? (yes/no): ").strip().lower()

    if start_game not in ['yes', 'y']:
        print("Exiting the game. Goodbye!")
        session.close()
        return

    # Ask how many AI players (1-5)
    while True:
        try:
            num_players = int(input("Enter the number of AI players (1-5): ").strip())
            if 1 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

    # Create a new Game instance
    game = Game(
        user_id=user.id,
        current_turn_number=1,
        total_turns=10, # need to make this changeable
        created_at=datetime.now(),
        is_active=True
    )
    session.add(game)
    session.commit()
    print(f"Game started with {num_players} AI players.")

    print("Game initialization in progress...")

    # Generate the initial world (countries and their data)
    generate_initial_world(game, num_players, session)

    # Generate initial marketplace data
    generate_marketplace_data(game.id, session)

    print("Game initialization complete.")

    # Start the game loop for each turn
    for turn_number in range(1, game.total_turns + 1):
        print(f"\n--- Turn {turn_number} ---")

        # Generate action options for all countries
        generate_action_options_for_all_countries(game, turn_number, session)

        # Process AI turns
        process_ai_turn(game, turn_number, session)

        # Update the current turn number in the game
        game.current_turn_number = turn_number
        session.commit()

    print("\nGame has ended after 50 turns.")

    # Determine the winner
    print("Determining the winner...")
    pick_winner(game.id, session)

    # Close the session
    session.close()

if __name__ == "__main__":
    main()
