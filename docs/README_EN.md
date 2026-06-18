# AgentTracker: Monitoring Middleware for AI Agents

A complete system for tracking, monitoring, and analyzing interactions between AI agents (such as CrewAI, AutoGen, LangChain, etc.) with automatic loop detection and cost calculation.

## 🎯 Main Features

### 1. **Message Tracking**
- Stores complete history of exchanged messages
- Records sender, recipient, content, timestamp, and tokens consumed
- Flexible queries on history

### 2. **Intelligent Loop Detection**
- **Advanced algorithm** that analyzes patterns in messages
- Detects identical or very similar messages (configurable similarity threshold)
- Signals repetitions (default: 3+ repetitions)
- Configurable exception or warning

### 3. **Cost Calculation**
- Estimates session cost based on tokens consumed
- Support for multiple models (GPT-4, GPT-3.5-turbo, custom)
- Input/output cost breakdown

### 4. **Analysis and Reporting**
- Complete session summary
- Export conversation to file
- Statistics per agent

---

## 📦 Installation

### Requirements
- Python 3.8+
- No external dependencies (standard library only)

### Setup
```bash
# Clone or copy files to your project
git clone <repository>
cd LoopHalter

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

---

## 🚀 Quick Start

### Basic Example
```python
from agent_tracker_en import AgentTracker, LoopDetectionException

# Create a tracker
tracker = AgentTracker()

# Add messages
try:
    tracker.add_message(
        sender="Agent_A",
        recipient="Agent_B",
        content="What is the meaning of life?",
        tokens_used=150
    )
    
    tracker.add_message(
        sender="Agent_B",
        recipient="Agent_A",
        content="The answer is 42",
        tokens_used=120
    )
    
except LoopDetectionException as e:
    print(f"❌ Loop detected: {e}")

# Get estimated cost
cost = tracker.estimate_session_cost(model="gpt-3.5-turbo")
print(f"💰 Total cost: ${cost['total_cost']:.6f}")

# Session summary
summary = tracker.get_conversation_summary()
print(f"📊 Total messages: {summary['total_messages']}")
```

---

## 📚 API Reference

### Class: `AgentTracker`

#### Initialization
```python
tracker = AgentTracker(
    max_loop_repetitions=3,      # Max repetitions before detecting loop
    similarity_threshold=0.85     # Similarity threshold (0-1)
)
```

#### Method: `add_message()`
Adds a message and checks for loops.

```python
result = tracker.add_message(
    sender: str,              # Sending agent ID
    recipient: str,           # Receiving agent ID
    content: str,             # Message content
    tokens_used: int = 0,     # Tokens consumed (optional)
    raise_on_loop: bool = True # Raise exception if loop detected
)

# Returns:
# {
#     "status": "success",
#     "message_count": int,
#     "loop_detected": bool,
#     "warning_message": str,
#     "loop_info": {...}
# }
```

#### Method: `estimate_session_cost()`
Calculates estimated session cost.

```python
cost = tracker.estimate_session_cost(model="gpt-3.5-turbo")

# Returns:
# {
#     "total_cost": float,      # Total cost in USD
#     "input_cost": float,      # Input cost
#     "output_cost": float,     # Output cost
#     "total_tokens": int,      # Total tokens
#     "input_tokens": int,
#     "output_tokens": int,
#     "model": str
# }
```

**Supported Models:**
- `"gpt-4"` - GPT-4 (most expensive, most powerful)
- `"gpt-3.5-turbo"` - GPT-3.5 Turbo (standard)
- `"default"` - Generic model

#### Method: `get_message_history()`
Retrieves message history with optional filters.

```python
# All messages
all_messages = tracker.get_message_history()

# Filter by sender
from_agent_a = tracker.get_message_history(sender="Agent_A")

# Filter by recipient
to_agent_b = tracker.get_message_history(recipient="Agent_B")

# Filter by both
conversation = tracker.get_message_history(
    sender="Agent_A",
    recipient="Agent_B"
)
```

#### Method: `get_conversation_summary()`
Provides a complete session summary.

```python
summary = tracker.get_conversation_summary()
print(summary)
# {
#     "total_messages": 5,
#     "agents_involved": ["Agent_A", "Agent_B", "Agent_C"],
#     "session_duration_seconds": 42.5,
#     "loop_detected": False,
#     "total_tokens": 750,
#     "estimated_cost": {...},
#     "message_count_by_agent": {"Agent_A": 3, "Agent_B": 2},
#     "start_time": "2024-06-18T10:30:00",
#     "end_time": "2024-06-18T10:30:42"
# }
```

#### Method: `export_conversation()`
Exports conversation to a text file.

```python
filename = tracker.export_conversation("conversation_log.txt")
print(f"Exported to: {filename}")
```

#### Method: `reset_session()`
Resets session state and clears history.

```python
tracker.reset_session()
# Now tracker is clean and ready for a new session
```

---

## 🔍 Loop Detection Algorithm

### How It Works
1. **Extraction**: Extracts last N messages between two agents (bidirectional)
2. **Similarity Calculation**: Uses `difflib.SequenceMatcher` to calculate similarity
3. **Pattern Analysis**: Detects repetitive patterns
4. **Reporting**: If found 3+ similar messages (configurable):
   - ✅ Option 1: Raises `LoopDetectionException`
   - ⚠️ Option 2: Emits warning

### Configurable Parameters
```python
tracker = AgentTracker(
    max_loop_repetitions=3,    # Number of repetitions before warning
    similarity_threshold=0.85   # Similarity threshold (0.0 = different, 1.0 = identical)
)
```

### Detection Example
```python
# These messages will trigger loop detector
messages = [
    "Can you repeat the question?",
    "Can you repeat the question?",
    "Can you repeat the question?",  # ⚠️ Loop detected!
]

for msg in messages:
    result = tracker.add_message(
        sender="Agent_A",
        recipient="Agent_B",
        content=msg,
        raise_on_loop=False  # Don't raise exception, just warn
    )
    
    if result["loop_detected"]:
        print(f"⚠️ {result['warning_message']}")
        print(f"   Repetitions: {result['loop_info']['repetitions']}")
```

---

## 💰 Cost System

### Predefined Cost Models
| Model | Input (per 1K tokens) | Output (per 1K tokens) |
|---------|----------------------|----------------------|
| GPT-4 | $0.03 | $0.06 |
| GPT-3.5-Turbo | $0.50 | $1.50 |
| Default | $0.01 | $0.02 |

### Calculation
```python
# Split 80% input / 20% output by default
cost = tracker.estimate_session_cost(model="gpt-4")
print(f"Input cost: ${cost['input_cost']:.6f}")
print(f"Output cost: ${cost['output_cost']:.6f}")
print(f"Total: ${cost['total_cost']:.6f}")
```

---

## 🔧 Framework Integration

### CrewAI
```python
from crewai_integration_en import TrackedCrewAIIntegration

integration = TrackedCrewAIIntegration()

agent_a.send_message(
    "agent_b",
    "Message",
    tokens=100
)

# Integration logs automatically!
status = integration.get_status()
integration.save_logs("crew_logs.json")
```

### Generic
```python
def your_agent_communication(sender, recipient, msg, tokens):
    tracker.add_message(sender, recipient, msg, tokens)
```

---

## 🧪 Testing

### Run Tests
```bash
# All tests
python -m unittest test_agent_tracker_en -v

# Specific tests
python -m unittest test_agent_tracker_en.TestLoopDetection -v
```

### Test Coverage
- ✅ 8 test classes
- ✅ 28+ unit tests
- ✅ Complete feature coverage

---

## 📖 Usage Examples

### Run Examples
```bash
python agent_tracker_en.py       # Basic example
python quickstart_en.py          # 7 use cases
python config_examples_en.py    # Configurations
```

---

## 🛠️ Troubleshooting

### Q: Loop detector is too sensitive
**A**: Increase `similarity_threshold` or `max_loop_repetitions`:
```python
tracker = AgentTracker(max_loop_repetitions=5, similarity_threshold=0.95)
```

### Q: Costs are not accurate
**A**: Provide actual consumed tokens:
```python
tracker.add_message(
    sender="Agent_A",
    recipient="Agent_B",
    content="Message",
    tokens_used=150  # Use the actual token count from the model
)
```

---

## 📄 License
MIT License - see LICENSE file

## 👥 Contributions
Pull requests and issue reports are welcome!

---

**Version**: 1.0.0  
**Last Update**: June 2024  
**Author**: AI Development Team
