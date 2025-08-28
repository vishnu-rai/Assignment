# Blackjack MCP Server Project - Complete Documentation

## Table of Contents

1. [What is MCP (Model Context Protocol)?](#what-is-mcp)
2. [How MCP Works](#how-mcp-works)
3. [Project Overview](#project-overview)
4. [Our Implementation Approach](#our-implementation-approach)
5. [Technical Architecture](#technical-architecture)
6. [Implementation Details](#implementation-details)
7. [Testing Strategy](#testing-strategy)
8. [State Persistence](#state-persistence)
9. [Interactive Gameplay](#interactive-gameplay)
10. [File Structure](#file-structure)
11. [Usage Guide](#usage-guide)
12. [Troubleshooting](#troubleshooting)

---

## What is MCP (Model Context Protocol)?

### Definition

MCP (Model Context Protocol) is an open standard protocol that enables AI models to interact with external tools, data sources, and systems. It provides a standardized way for Large Language Models (LLMs) to access and manipulate real-world data and perform actions through a client-server architecture.

### Key Concepts

- **Protocol**: A standardized communication format between clients and servers
- **Client-Server Architecture**: LLMs act as clients, tools act as servers
- **Tool Integration**: Allows LLMs to use external tools and data sources
- **Standardization**: Provides consistent interface across different tools and systems

### Why MCP?

- **Interoperability**: Works with any LLM that supports MCP
- **Extensibility**: Easy to add new tools and capabilities
- **Security**: Controlled access to external systems
- **Flexibility**: Supports various communication methods (stdio, HTTP, WebSocket)

---

## How MCP Works

### Architecture Overview

```
┌─────────────────┐    JSON-RPC    ┌─────────────────┐
│   LLM Client    │ ◄────────────► │  MCP Server     │
│  (Claude, etc.) │                │  (Our Tools)    │
└─────────────────┘                └─────────────────┘
```

### Communication Flow

1. **Initialization**: Client sends `initialize` request to server
2. **Tool Discovery**: Client requests available tools via `tools/list`
3. **Tool Execution**: Client calls tools via `tools/call` with parameters
4. **Response**: Server returns results in standardized format

### JSON-RPC Protocol

```json
// Client Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "deal",
    "arguments": {"bet": 25}
  }
}

// Server Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{
      "type": "text",
      "text": "Dealt new hands with bet $25"
    }]
  }
}
```

---

## Project Overview

### Objective

Create a Blackjack game server using MCP that allows:

1. **LLM vs Dealer**: AI plays Blackjack against the dealer
2. **Interactive Play**: Users play using natural language
3. **State Persistence**: Game state saved across sessions
4. **Complete Game Logic**: Full Blackjack implementation

### Key Features

- ✅ Complete Blackjack game implementation
- ✅ MCP stdio server with 7 tools
- ✅ State persistence across sessions
- ✅ LLM integration (Claude Haiku)
- ✅ Interactive natural language gameplay
- ✅ Comprehensive testing suite
- ✅ Error handling and validation

---

## Our Implementation Approach

### Phase 1: Basic MCP Server

**Goal**: Create a working MCP server with basic Blackjack functionality

**Approach**:

1. **Research MCP Protocol**: Studied JSON-RPC specification and MCP standards
2. **Choose Implementation Method**: Direct JSON-RPC handling vs MCP SDK
3. **Initial Implementation**: Started with MCP SDK but encountered issues
4. **Pivot to Direct Implementation**: Implemented JSON-RPC protocol directly

**Challenges & Solutions**:

- **Challenge**: MCP SDK parameter validation errors
- **Solution**: Implemented direct JSON-RPC handling for better control
- **Challenge**: State management across server restarts
- **Solution**: Added file-based state persistence

### Phase 2: Game Logic Implementation

**Goal**: Implement complete Blackjack game rules

**Approach**:

1. **Core Game Logic**: Card dealing, hand calculation, dealer rules
2. **Tool Definitions**: Created 7 MCP tools for all game actions
3. **Error Handling**: Input validation and error responses
4. **Game State Management**: Track hands, scores, bets, round status

**Key Decisions**:

- **Ace Handling**: 11 or 1 based on best hand value
- **Dealer Rules**: Hit on 16 and below, stand on 17 and above
- **Bet Limits**: $1-$100 range for realistic gameplay
- **Deck Management**: Support 0-6 decks with auto-shuffle

### Phase 3: LLM Integration

**Goal**: Enable LLM to play Blackjack strategically

**Approach**:

1. **MCP Client Setup**: Configured MCP client to connect to our server
2. **LLM Configuration**: Used Claude Haiku with strategic prompts
3. **Tool Integration**: LLM uses MCP tools to play the game
4. **Strategic Decision Making**: Implemented Blackjack basic strategy

**LLM Strategy**:

- Hit on totals of 16 or below
- Stand on hard totals of 17 or above
- Consider dealer's up card in decisions
- Follow basic Blackjack strategy

### Phase 4: State Persistence

**Goal**: Maintain game state across server restarts

**Approach**:

1. **State File Design**: JSON structure for all game data
2. **Save Operations**: Save state after each game action
3. **Load Operations**: Restore state on server startup
4. **File Path Management**: Ensure consistent state file location

**State Data**:

```json
{
  "deck": ["A♠", "K♥", ...],
  "player_hand": ["10♦", "7♣"],
  "dealer_hand": ["A♠", "??"],
  "player_score": 25,
  "current_bet": 25,
  "in_round": true,
  "num_decks": 6
}
```

### Phase 5: Interactive Gameplay

**Goal**: Create natural language interface for human players

**Approach**:

1. **Interactive Script**: Created `play.py` for user interaction
2. **Natural Language Processing**: LLM interprets user commands
3. **Conversational Interface**: Friendly, helpful dealer assistant
4. **Command Examples**: Provided clear usage examples

**User Commands**:

- "I want to start a new game"
- "Deal me a hand with $25"
- "I want to hit"
- "I'll stand"
- "What's my score?"
- "Show me the current game"

---

## Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
├─────────────────────────────────────────────────────────────┤
│  play.py (Interactive)  │  chat.py (LLM vs Dealer)         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    MCP Client Layer                         │
├─────────────────────────────────────────────────────────────┤
│  MCPClient (mcp-use)  │  MCPAgent (LLM Integration)        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server Layer                         │
├─────────────────────────────────────────────────────────────┤
│  main.py (Blackjack Server)  │  JSON-RPC Protocol           │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Game Logic Layer                         │
├─────────────────────────────────────────────────────────────┤
│  BlackJack Class  │  Card Logic  │  State Management        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Persistence Layer                        │
├─────────────────────────────────────────────────────────────┤
│  blackjack_state.json  │  File I/O Operations               │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → Natural language command
2. **LLM Processing** → Command interpretation and tool selection
3. **MCP Client** → JSON-RPC request to server
4. **MCP Server** → Tool execution and game logic
5. **State Update** → Game state modification and persistence
6. **Response** → Result back through the chain to user

---

## Implementation Details

### MCP Server Implementation (`main.py`)

#### Core Components

```python
class BlackJack:
    def __init__(self):
        # Game state initialization
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_score = 0
        self.current_bet = 0
        self.in_round = False
        self.num_decks = 1

        # Load existing state or initialize new game
        saved_state = load_state()
        if saved_state:
            # Restore from saved state
        else:
            # Initialize new game
```

#### Tool Definitions

```python
TOOLS = [
    {
        "name": "reset",
        "description": "Reset the current score to zero for the player",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "shuffle",
        "description": "Reshuffle with the given number of decks (0-6)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "num_decks": {
                    "type": "integer",
                    "description": "Number of decks to use (0-6)",
                    "minimum": 0,
                    "maximum": 6
                }
            },
            "required": ["num_decks"]
        }
    },
    # ... additional tools
]
```

#### JSON-RPC Handler

```python
def main():
    """Simple MCP server implementation."""
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())

            if request.get("method") == "initialize":
                # Handle initialization
            elif request.get("method") == "tools/list":
                # Return available tools
            elif request.get("method") == "tools/call":
                # Execute tool and return result
            else:
                # Return method not found error
```

### State Persistence Implementation

#### Save State Function

```python
def save_state(game_state):
    """Save game state to file."""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(game_state, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save state: {e}", file=sys.stderr)
```

#### Load State Function

```python
def load_state():
    """Load game state from file."""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load state: {e}", file=sys.stderr)
    return None
```

### LLM Integration Implementation

#### MCP Client Setup

```python
# Initialize MCP client with Blackjack server
client = MCPClient.from_config_file("../mcp-server-config.json")
llm = ChatAnthropic(model="claude-3-5-haiku-20241022")

# Create agent with specific system prompt
agent = MCPAgent(
    llm=llm,
    client=client,
    max_steps=20,
    system_prompt=system_prompt
)
```

#### System Prompt Design

```python
system_prompt = """You are playing a game of Blackjack against the dealer. You have access to the following tools:

1. reset - Reset your score to zero
2. shuffle(num_decks) - Shuffle the deck (0-6 decks)
3. deal(bet) - Deal new hands with a bet (1-100)
4. hit - Take another card
5. stand - End your turn and let dealer play
6. score - Check your current score

GAME RULES:
- Get as close to 21 as possible without going over
- Face cards (J, Q, K) are worth 10
- Aces are worth 11 or 1 (whichever is better for your hand)
- Dealer must hit on 16 and below, stand on 17 and above
- If you go over 21, you bust and lose
- If dealer goes over 21, you win
- Higher hand wins, ties result in push (bet returned)

STRATEGY:
- Always hit on 8 or below
- Hit on soft totals (with Ace) of 17 or below
- Stand on hard totals of 17 or above
- Consider the dealer's up card when making decisions

IMPORTANT: You MUST complete the full game round. After dealing, make your decisions (hit/stand), then call the score tool to show the final result. Do not stop until you've completed the entire round and shown the final score."""
```

---

## Testing Strategy

### Automated Testing (`test.py`)

- **Server Initialization**: Verify MCP server starts correctly
- **Tool Functionality**: Test each of the 7 MCP tools
- **Game Logic**: Verify Blackjack rules implementation
- **Error Handling**: Test invalid inputs and edge cases

### Test Commands

```python
test_commands = [
    ("reset", {}, "Reset player score"),
    ("shuffle", {"num_decks": 1}, "Shuffle deck with 1 deck"),
    ("deal", {"bet": 25}, "Deal hand with $25 bet"),
    ("hit", {}, "Player hits"),
    ("stand", {}, "Player stands"),
    ("score", {}, "Get player score")
]
```

### Manual Testing

- **LLM Game**: Test AI gameplay with `./llm_play.sh`
- **Interactive Game**: Test human interaction with `./play_game.sh`
- **State Persistence**: Verify state saves and loads correctly
- **Error Scenarios**: Test invalid commands and edge cases

---

## State Persistence

### Design Decisions

1. **File Format**: JSON for human readability and debugging
2. **Location**: Root directory for consistent access
3. **Content**: Complete game state including deck, hands, scores
4. **Frequency**: Save after every game action
5. **Error Handling**: Graceful degradation if save/load fails

### State File Structure

```json
{
  "deck": ["A♠", "K♥", "Q♦", ...],
  "player_hand": ["10♣", "7♠"],
  "dealer_hand": ["A♠", "??"],
  "player_score": 25,
  "current_bet": 25,
  "in_round": true,
  "num_decks": 6
}
```

### Implementation Benefits

- **Session Continuity**: Resume games across server restarts
- **Debugging**: Easy to inspect game state
- **Recovery**: Can manually edit state file if needed
- **Transparency**: Clear view of current game status

---

## Interactive Gameplay

### Design Philosophy

- **Natural Language**: Users speak naturally, not technical commands
- **Conversational**: LLM acts as helpful dealer assistant
- **Guided Experience**: LLM provides context and suggestions
- **Error Prevention**: LLM guides users through proper game flow

### User Experience Flow

1. **Welcome**: Clear instructions and examples
2. **Status Check**: LLM checks current game state
3. **Command Processing**: Natural language interpretation
4. **Action Execution**: MCP tool execution
5. **Response**: Clear explanation of what happened
6. **Guidance**: Suggestions for next steps

### Example Interaction

```
🎯 Your turn: Deal me a hand with $25

🤖 Processing: 'Deal me a hand with $25'
------------------------------
You've been dealt a hand with a bet of $25. Your current hand is:
- 8 of Diamonds
- 7 of Spades

Your hand's total value is 15. The dealer is showing a King of Spades, with their second card face down.

At this point, you have a few options:
1. Hit (take another card)
2. Stand (keep your current hand)

What would you like to do? Remember, your goal is to get as close to 21 as possible without going over.
```

---

## File Structure

```
project_mcp_game_start_vishnu-rai/
├── main.py                     # MCP Blackjack server
├── test.py                     # Automated test suite
├── run_test.sh                # Test runner script
├── llm_play.sh                # LLM vs Dealer game runner
├── play_game.sh               # Interactive game runner
├── blackjack_state.json       # Game state persistence
├── mcp-server-config.json     # MCP server configuration
├── python/
│   ├── chat.py                # LLM integration script
│   └── play.py                # Interactive gameplay script
├── mcp-use/                   # MCP client library
├── venv/                      # Python virtual environment
├── .env                       # Environment variables
└── README.md                  # Project documentation
```

### Key Files Explained

#### `main.py`

- **Purpose**: MCP stdio server implementation
- **Features**: Complete Blackjack game logic, state persistence, JSON-RPC handling
- **Tools**: 7 MCP tools for all game actions

#### `test.py`

- **Purpose**: Automated testing of MCP server
- **Features**: Tests all tools, game logic, error handling
- **Output**: Detailed test results and success/failure reporting

#### `play.py`

- **Purpose**: Interactive natural language gameplay
- **Features**: User input processing, LLM integration, conversational interface
- **Flow**: Welcome → Status → Commands → Responses → Guidance

#### `chat.py`

- **Purpose**: LLM vs Dealer gameplay
- **Features**: Strategic AI gameplay, complete game rounds
- **Strategy**: Basic Blackjack strategy implementation

---

## Usage Guide

### Prerequisites

1. **Python 3.11+**: Required for MCP and dependencies
2. **Virtual Environment**: Isolated Python environment
3. **API Key**: Anthropic API key for LLM integration
4. **Dependencies**: MCP, LangChain, Anthropic packages

### Setup Instructions

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -e .

# 3. Set up API key
cp mcp-use/.env.example mcp-use/.env
# Edit mcp-use/.env and add your ANTHROPIC_API_KEY

# 4. Test installation
./run_test.sh
```

### Running the Game

#### Automated Testing

```bash
./run_test.sh
```

#### LLM vs Dealer Game

```bash
./llm_play.sh
```

#### Interactive Human Game

```bash
./play_game.sh
```

### Game Commands

#### Natural Language Commands

- "I want to start a new game"
- "Deal me a hand with $25"
- "I want to hit"
- "I'll stand"
- "What's my score?"
- "Show me the current game"
- "quit"

#### Direct MCP Commands

```bash
# Initialize server
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}' | python main.py

# Reset score
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "reset", "arguments": {}}}' | python main.py

# Deal hand
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "deal", "arguments": {"bet": 25}}}' | python main.py
```

---

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'mcp_use'`
**Solution**:

```bash
source venv/bin/activate
pip install mcp-use langchain-anthropic
```

#### 2. API Key Issues

**Problem**: `Error code: 401 - invalid x-api-key`
**Solution**:

```bash
# Check API key in mcp-use/.env
cat mcp-use/.env
# Ensure ANTHROPIC_API_KEY is set correctly
```

#### 3. State File Issues

**Problem**: Multiple state files or wrong location
**Solution**:

```bash
# Check for duplicate state files
find . -name "blackjack_state.json"
# Remove duplicates, keep only root directory version
```

#### 4. Permission Issues

**Problem**: Scripts not executable
**Solution**:

```bash
chmod +x run_test.sh llm_play.sh play_game.sh
```

### Debug Mode

Enable verbose logging:

```bash
export MCP_USE_DEBUG=true
./play_game.sh
```

### State File Inspection

```bash
# View current game state
cat blackjack_state.json

# Reset game state
rm blackjack_state.json
```

---

## Technical Decisions and Rationale

### 1. Direct JSON-RPC Implementation vs MCP SDK

**Decision**: Implemented JSON-RPC protocol directly
**Rationale**:

- Better control over error handling
- Avoided SDK parameter validation issues
- More transparent debugging
- Easier to understand and modify

### 2. File-Based State Persistence

**Decision**: JSON file for state storage
**Rationale**:

- Human readable for debugging
- No database setup required
- Easy to backup and restore
- Transparent state inspection

### 3. Natural Language Interface

**Decision**: LLM as conversational dealer assistant
**Rationale**:

- More user-friendly than technical commands
- Handles edge cases and errors gracefully
- Provides helpful guidance and context
- Mimics real casino experience

### 4. Comprehensive Testing

**Decision**: Automated test suite with manual testing
**Rationale**:

- Ensures reliability across changes
- Validates all game logic
- Provides confidence in deployment
- Documents expected behavior

---

## Future Enhancements

### Potential Improvements

1. **Web Interface**: Browser-based UI for easier access
2. **Multiplayer Support**: Multiple players at same table
3. **Advanced Strategies**: Card counting, side bets
4. **Statistics Tracking**: Win/loss ratios, betting patterns
5. **Customization**: Different rule variations
6. **AI Improvements**: More sophisticated decision making

### Scalability Considerations

1. **Database Storage**: Replace file-based state with database
2. **Multiple Instances**: Support concurrent game sessions
3. **Load Balancing**: Distribute games across servers
4. **Caching**: Improve response times for frequent operations

---

## Conclusion

This project demonstrates a complete implementation of an MCP server for a Blackjack game, showcasing:

1. **MCP Protocol Mastery**: Understanding and implementing the Model Context Protocol
2. **Game Logic Implementation**: Complete Blackjack rules and mechanics
3. **State Management**: Persistent game state across sessions
4. **LLM Integration**: Strategic AI gameplay using Claude Haiku
5. **User Experience**: Natural language interface for human players
6. **Testing Strategy**: Comprehensive validation and error handling
7. **Documentation**: Complete technical and user documentation

The project successfully combines modern AI capabilities with traditional game mechanics, creating an engaging and educational experience that demonstrates the power and flexibility of the MCP protocol for building AI-powered applications.

---

## References

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Blackjack Rules](https://bicyclecards.com/how-to-play/blackjack/)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [LangChain Documentation](https://python.langchain.com/)
- [Anthropic Claude API](https://docs.anthropic.com/)
