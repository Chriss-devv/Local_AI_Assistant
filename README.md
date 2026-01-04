# AI Assistant v7.82

A customizable AI assistant with contextual web search, intelligent query enrichment, and auto-save functionality.

![Version](https://img.shields.io/badge/version-7.82-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## Features

### Complete Customization
- **Setup wizard** on first run
- Customizable assistant and user names
- Adjustable role and personality
- Configurable logs directory
- Adjustable auto-save interval

### Contextual Web Search (v7.82)
- **Intelligent enrichment**: "search improve it" → "search improve Python code"
- **Conversational context**: Automatically includes last 3 exchanges
- **Optimized queries**: Detects vague references and enriches them
- **Direct implementation**: Generates code based on search results

### Temporal Awareness
- Knows what day is TODAY, YESTERDAY, and TOMORROW
- Prioritizes information from current year (2026)
- Requests web searches for recent events

### Intelligent Auto-Save
- Automatically saves sessions every N messages
- Logs in Markdown format
- Complete conversation history

### Multi-Line Mode
- Paste complete code using ` ``` `
- Preserves indentation and formatting
- Perfect for code review/improvement

### Model Hot-Swapping
- Change model mid-conversation
- Preserves entire history
- Supports any Ollama model

---

## Installation

### Prerequisites

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Download a model
ollama pull llama3.2:latest
# or
ollama pull mistral:latest
```

### Assistant Installation

```bash
# Clone repository
git clone https://github.com/[your-username]/ai-assistant.git
cd ai-assistant

# Install dependencies
pip install ollama ddgs

# Run for first time (setup wizard)
python3 assistant.py
```

---

## Usage

### First Run

On first execution, you'll see the setup wizard:

```
AI Assistant v7.82 - Customizable
============================================================

INITIAL SETUP - AI Assistant v7.82
============================================================

Welcome! Let's customize your assistant.

What would you like to name your assistant? [Assistant]: Jarvis
What is your name? [User]: Chris

What role should your assistant have?
  1. Technical/Programming assistant
  2. General/Conversational assistant
  3. Educational tutor
  4. Custom
Select [1-4]: 1

Configuration saved!
```

### Available Commands

| Command | Description |
|---------|-------------|
| `exit` / `quit` | Terminate and save session |
| `clear` | Clear conversation memory |
| `save` | Manually save session |
| `model` | Change model (preserves history) |
| `models` | List available models |
| `search <query>` | Manual web search |
| ` ``` ` | Multi-line mode (end with ```) |
| `config` | Reconfigure assistant |

---

## Usage Examples

### Example 1: Contextual Web Search

```
User> give me code to scan network with Python

[Assistant]: Here's a script using Scapy...
```python
import scapy.all as scapy
...
```

User> search how to improve it
🌐 Searching: 'search how to improve it'...
   Enhanced query: 'how to improve Python network scan code'
   With conversational context
   Found 10 results

[Assistant]: Based on the results, here's the improved code:
```python
import scapy.all as scapy
import argparse
# [complete improved code]
```
Now understands context and generates solution!
```

### Example 2: Multi-Line Mode

```
User> ```
Multi-line mode activated...
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
```
Code captured (4 lines)

User> optimize this
[Assistant]: Here's the optimized version with memoization...
```

### Example 3: Model Change

```
User> model

Current model: llama3.2:latest

Available models:
------------------------------------------------------------
> 1. llama3.2:latest                   (2.02 GB)
  2. mistral:latest                    (4.11 GB)
  3. codellama:latest                  (3.83 GB)
------------------------------------------------------------

Select new model [1-3]: 2
Conversation history preserved
```

---

## Configuration

Configuration is saved in `~/.ai_assistant/config.json`:

```json
{
  "assistant_name": "Assistant",
  "user_name": "User",
  "timezone": "America/New_York",
  "logs_dir": "/home/user/.ai_assistant/logs",
  "max_messages_context": 20,
  "auto_save_interval": 10,
  "assistant_role": "AI assistant",
  "user_expertise": "technical user",
  "language": "English",
  "temperature": 0.7,
  "top_p": 0.9,
  "num_ctx": 8192,
  "num_predict": 800
}
```

### Editable Parameters

- **assistant_name**: Assistant's name
- **user_name**: Your name
- **logs_dir**: Logs directory
- **max_messages_context**: Sliding window size
- **auto_save_interval**: Auto-save every N messages
- **assistant_role**: Assistant's role
- **temperature**: Creativity (0.0 = deterministic, 1.0 = creative)
- **top_p**: Response diversity
- **num_ctx**: Context tokens
- **num_predict**: Max response tokens

---

## File Structure

```
~/.ai_assistant/
├── config.json          # Custom configuration
└── logs/               # Session logs
    ├── session_20260104_120000.md
    ├── session_20260104_130000.md
    └── ...
```

### Log Format

```markdown
# Assistant Session - 2026-01-04 12:00:00

**User**: User  
**Model**: llama3.2:latest  
**Messages**: 15  
**Model changes**: 0

---

## Conversation

### > User (Message #1)
Hello

### [Assistant] Response #1
Hello! How can I help you?
```

---

## Troubleshooting

### Error: "No models found installed"

```bash
# Solution: Install a model
ollama pull llama3.2:latest
```

### Error: "Is Ollama running?"

```bash
# Solution: Start Ollama
ollama serve
# or verify
ollama list
```

### Error: "ModuleNotFoundError: No module named 'ddgs'"

```bash
# Solution: Install dependency
pip install ddgs
```

---

## Development

### Testing

```bash
# Verify syntax
python3 -m py_compile assistant.py

# Run in debug mode
python3 assistant.py
```

### Contributing

1. Fork the project
2. Create a branch: `git checkout -b feature/new-feature`
3. Commit: `git commit -m 'Add new feature'`
4. Push: `git push origin feature/new-feature`
5. Open a Pull Request

---

## Changelog

### v7.82 (2026-01-04)
- Intelligent query enrichment
- Direct action system prompt
- Generates code based on searches
- Fix: Passivity when receiving search data

### v7.8 (2026-01-04)
- Vague query enrichment
- "improve it" → "how to improve [context]"
- Visual feedback for improved queries

### v7.75 (2026-01-04)
- Universal contextual search
- Context in ALL searches
- New `extract_conversational_context()` function

### v7.7 (2026-01-04)
- Improved temporal context
- Explicit TODAY/YESTERDAY/TOMORROW
- Fix: Date variables correctly expanded

### v7.65 (2026-01-04)
- Contextual search (manual command)
- Auto-save every 10 messages

### v7.6 (2026-01-03)
- Multi-line mode with ` ``` `
- Model hot-swapping
- Intelligent auto-search

---

## License

MIT License - Use, modify, and share freely.

---

## Acknowledgments

- **Ollama Team** - For the local LLM platform
- **DuckDuckGo** - For the search API
- Based on **Jarvis** architecture

---

## Support

Problems or suggestions?

1. Open an [issue on GitHub](https://github.com/[your-username]/ai-assistant/issues)
2. Review the [documentation](#usage)
3. Check the [troubleshooting](#troubleshooting) section

---

**AI Assistant v7.82 - Your customizable assistant with local AI**
