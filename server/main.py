# main.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Game
from datetime import datetime
import os

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

    # Ask how many AI players (max 5)
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
        total_turns=50,
        created_at=datetime.now(),
        is_active=True
    )
    session.add(game)
    session.commit()
    print(f"Game started with {num_players} AI players.")

    # Placeholder for initiating the game generation process
    # You can implement your game initialization logic here
    # For example:
    # generate_initial_world(game, num_players, session)

    print("Game initialization in progress...")

    # Close the session
    session.close()

if __name__ == "__main__":
    main()
