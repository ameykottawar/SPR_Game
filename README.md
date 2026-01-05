🎮 SPR_Game — Rock-Paper-Scissors-Plus Game Bot

Assignment Submission | upliance.ai — AI Product Engineer Role

An AI-powered referee for a Rock-Paper-Scissors game with a twist:
each player gets one special “bomb” move that beats all other moves.

Built using Google’s Agent Development Kit (ADK) with explicit tool-based architecture and clear separation of concerns.

🚀 Quick Start
Installation
pip install google-adk

Setup API Key
echo "GOOGLE_API_KEY=your_key_here" > rps_plus_agent/.env

Run the Game
adk run rps_plus_agent

🧠 How It Works

The system is implemented as an AI agent acting as a game referee, coordinating intent understanding, game logic, and response generation using ADK tools.

🗂️ State Management

Game state is managed via a GameState class that tracks:

Current round number (1–3)

Player and bot scores

Whether each player has used their bomb

Game-over status

The state is stored as a global in-memory variable, which is sufficient for a single-session CLI game.
Importantly, state is not embedded in prompts—it is managed exclusively via tools.

🛠️ Tools Design

The game logic is broken into six explicit tools, each with a single responsibility:

1. validate_move(move)

Verifies if the move is legal

Checks:

Is it a valid move type?

Has the bomb already been used?

2. resolve_round(user_move, bot_move)

Pure game logic

Determines the round winner

No side effects (no state mutation)

3. update_game_state(user_move, bot_move, winner)

Updates:

Scores

Round count

Bomb usage flags

Only tool that mutates state

4. get_bot_move()

Bot strategy:

Round 1: Random (rock/paper/scissors)

Rounds 2–3:

30% chance to use bomb if available

Otherwise random standard move

5. get_game_status()

Allows the agent to inspect the current game state

Read-only, no mutations

6. reset_game()

Clears state to start a fresh game

🏗️ Architecture

The agent cleanly separates responsibilities:

Intent Understanding
The LLM interprets the user’s input.

Game Logic
Tools validate moves and apply rules.

Response Generation
The LLM formats human-readable output.

Agent Workflow

Check game status

Get user move

Validate move

Generate bot move

Resolve round

Update game state

Display results

Repeat or end game

🎯 Design Decisions
Why global state?

For a simple CLI game, global state is straightforward and effective.
In production, this would be replaced with session-based or persistent storage.

Why separate resolve_round and update_game_state?

resolve_round is pure and testable

State changes are isolated to one tool

Improves clarity and maintainability

Why a strategic bot?

Prevents trivial gameplay and avoids wasting the bomb in early rounds.

Invalid input handling

Invalid moves consume a round, as required

The agent explains the error

State is still updated via update_game_state

⚖️ Trade-offs
Chosen Approach

✅ Simple, readable code
✅ Clear separation of concerns
✅ Explicit tool usage
✅ Easy to test logic independently

Limitations

❌ Global state not suitable for multi-user scenarios

🔧 Future Improvements

With more time, I would add:

Session-based state management using ADK sessions

Unit tests for each tool

Smarter bot AI (pattern detection, adaptive play)

Graceful error handling (API/network issues)

Move history tracking for analysis/replay

Configurable rules (best-of-5, new move types)

🧪 Testing Notes

Tested using open-source models via the Google AI API

Core logic, state handling, and tool orchestration work as expected

Encountered Gemini free-tier rate limits during final testing

This was an API quota issue, not a code issue

For demonstration, the project uses:

gemini-1.5-flash-8b


which should work within free-tier limits if quota is available.

📁 Project Structure
rps_project/
├── rps_plus_agent/
│   ├── __init__.py        # Package initialization
│   ├── agent.py           # Main game implementation
│   └── .env               # API key configuration
└── README.md              # Project documentation

✅ Requirements Met

✅ Best-of-3 rounds with auto-termination

✅ Rock / Paper / Scissors / Bomb moves

✅ Bomb usable once per player

✅ Invalid input wastes a round

✅ State persists outside prompts

✅ Multiple explicit tools

✅ Clean architectural separation

✅ Python + Google ADK

✅ No databases, APIs, or UI frameworks
