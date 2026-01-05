import random
from typing import Literal
from google.adk.agents import Agent
from pydantic import BaseModel, Field


# Game state model
class GameState(BaseModel):
    round_number: int = Field(default=1)
    user_score: int = Field(default=0)
    bot_score: int = Field(default=0)
    user_bomb_used: bool = Field(default=False)
    bot_bomb_used: bool = Field(default=False)
    game_over: bool = Field(default=False)
    last_user_move: str = Field(default="")
    last_bot_move: str = Field(default="")
    last_round_result: str = Field(default="")


# Store game state in memory
game_state = GameState()


def validate_move(move: str) -> dict:
    """Check if a move is valid given current game state."""
    move = move.lower().strip()
    
    valid_moves = ["rock", "paper", "scissors", "bomb"]
    if move not in valid_moves:
        return {
            "valid": False,
            "normalized_move": "",
            "message": f"'{move}' is not a valid move. Choose: rock, paper, scissors, or bomb"
        }
    
    if move == "bomb" and game_state.user_bomb_used:
        return {
            "valid": False,
            "normalized_move": "",
            "message": "You already used your bomb! Choose rock, paper, or scissors"
        }
    
    return {
        "valid": True,
        "normalized_move": move,
        "message": "Valid move"
    }


def resolve_round(user_move: str, bot_move: str) -> dict:
    """Determine round winner based on game rules."""
    
    # Bomb logic
    if user_move == "bomb" and bot_move == "bomb":
        return {
            "winner": "draw",
            "explanation": "Both used bomb - draw!"
        }
    
    if user_move == "bomb":
        return {
            "winner": "user",
            "explanation": "Your bomb destroys everything!"
        }
    
    if bot_move == "bomb":
        return {
            "winner": "bot",
            "explanation": "My bomb destroys everything!"
        }
    
    # Same move = draw
    if user_move == bot_move:
        return {
            "winner": "draw",
            "explanation": f"Both picked {user_move}!"
        }
    
    # Standard rock-paper-scissors
    wins_against = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }
    
    if wins_against[user_move] == bot_move:
        return {
            "winner": "user",
            "explanation": f"{user_move.title()} beats {bot_move}!"
        }
    
    return {
        "winner": "bot",
        "explanation": f"{bot_move.title()} beats {user_move}!"
    }


def update_game_state(user_move: str, bot_move: str, round_winner: Literal["user", "bot", "draw"]) -> dict:
    """Update game state after a round completes."""
    global game_state
    
    game_state.last_user_move = user_move
    game_state.last_bot_move = bot_move
    
    # Track bomb usage
    if user_move == "bomb":
        game_state.user_bomb_used = True
    if bot_move == "bomb":
        game_state.bot_bomb_used = True
    
    # Update scores
    if round_winner == "user":
        game_state.user_score += 1
        game_state.last_round_result = "You won the round"
    elif round_winner == "bot":
        game_state.bot_score += 1
        game_state.last_round_result = "Bot won the round"
    else:
        game_state.last_round_result = "Round was a draw"
    
    # Move to next round
    game_state.round_number += 1
    
    # Check if game should end
    if game_state.round_number > 3:
        game_state.game_over = True
    
    return {
        "round_completed": game_state.round_number - 1,
        "current_score": f"{game_state.user_score}-{game_state.bot_score}",
        "game_over": game_state.game_over,
        "rounds_left": max(0, 4 - game_state.round_number)
    }


def get_bot_move() -> dict:
    """Decide bot's move with basic strategy."""
    
    # Don't waste bomb on round 1
    if game_state.round_number == 1:
        return {"move": random.choice(["rock", "paper", "scissors"])}
    
    # Use bomb strategically in later rounds (30% chance)
    if not game_state.bot_bomb_used and random.random() < 0.3:
        return {"move": "bomb"}
    
    # Otherwise play randomly
    moves = ["rock", "paper", "scissors"]
    return {"move": random.choice(moves)}


def get_game_status() -> dict:
    """Get current game state."""
    return {
        "round": game_state.round_number,
        "score": f"{game_state.user_score}-{game_state.bot_score}",
        "user_bomb_available": not game_state.user_bomb_used,
        "bot_bomb_available": not game_state.bot_bomb_used,
        "game_over": game_state.game_over,
        "last_result": game_state.last_round_result
    }


def reset_game() -> dict:
    """Start a fresh game."""
    global game_state
    game_state = GameState()
    return {"status": "New game started", "ready": True}


# Agent configuration
root_agent = Agent(
    name="rps_game_referee",
    model="gemini-1.5-flash-8b",
    description="Referee for Rock-Paper-Scissors-Plus with bomb move",
    instruction="""You're refereeing Rock-Paper-Scissors-Plus. Keep it simple and fun.

Rules (explain briefly at start):
- Best of 3 rounds
- Moves: rock, paper, scissors, bomb
- Bomb beats everything (except another bomb = draw)
- Each player gets ONE bomb per game
- Invalid moves waste a round

How to run the game:
1. Start by checking game_status
2. Ask for the user's move
3. Validate their move with validate_move
4. Get the bot's move with get_bot_move
5. Resolve who won with resolve_round
6. Update state with update_game_state
7. Show round results clearly (round number, moves, winner)
8. After round 3, end game and show final score

For invalid moves: explain the problem but still count it as a round.

Keep responses concise and friendly.""",
    tools=[
        validate_move,
        resolve_round,
        update_game_state,
        get_bot_move,
        get_game_status,
        reset_game
    ]
)
