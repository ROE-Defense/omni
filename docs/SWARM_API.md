# Omni Swarm API (v0.7.0)

The Swarm is the nervous system of Omni. It allows specialized agents to communicate asynchronously, share context, and solve complex problems collaboratively.

## 1. The Core Concept
Instead of a single monolithic LLM prompt, Omni uses a **Message Bus**.
*   **User:** Sends a message to `@roe/architect`.
*   **Architect:** Thinks, then sends a sub-task to `@roe/backend`.
*   **Backend:** Executes code, then replies to Architect.
*   **Architect:** Compiles results and replies to User.

## 2. Message Protocol
All communication uses the `SwarmMessage` schema.

```json
{
  "id": "uuid-v4",
  "timestamp": 1707123456.789,
  "sender": "@roe/architect",
  "recipient": "@roe/backend",
  "type": "instruction", 
  "payload": {
    "task": "Create a User model with UUID primary key."
  }
}
```

### Message Types
*   `instruction`: A command to perform an action.
*   `artifact`: The result of an action (code, text, file path).
*   `error`: Something went wrong.

## 3. Python SDK
To create a custom agent, import the `SwarmAgent` class.

```python
from swarm.bus import OmniBus
from swarm.agent import SwarmAgent

# 1. Connect to Bus
bus = OmniBus()

# 2. Define Custom Logic
def my_custom_brain(system, user):
    return "I am a custom agent!"

# 3. Register Agent
agent = SwarmAgent(
    name="@my/custom-agent",
    bus=bus,
    llm_client=my_custom_brain,
    system_prompt="You are a custom agent."
)

# 4. Send Message
agent.send("@roe/backend", {"task": "Hello"})
```

## 4. The Router
In `omni.py`, the `OmniAgent` acts as the Router. It analyzes user intent and dispatches the first message to the most relevant specialized agent.

## 5. Future Roadmap (v0.8.0)
*   **Vector Memory:** Agents will read/write shared context to LanceDB.
*   **Capabilities Registry:** Agents will broadcast what they can do (e.g., "I can run Python").
*   **Swarm UI:** A visual graph of agent interactions.
