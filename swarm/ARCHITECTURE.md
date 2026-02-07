# Omni Swarm Architecture (v0.7.0)

**Objective:** Enable autonomous collaboration between specialized brains without human intervention.

## 1. The Core Concept
The Swarm is a **local-only, peer-to-peer agent bus**. It replaces the monolithic LLM context window with a distributed system where specialized agents (Architect, Backend, Frontend) exchange structured messages to solve complex problems.

## 2. The Omni Bus Protocol
Agents communicate via a standardized JSON schema over a local message queue (ZeroMQ or internal Python Queue).

### Message Schema
```json
{
  "id": "uuid-v4",
  "timestamp": 1707123456,
  "sender": "@roe/architect",
  "recipient": "@roe/backend",
  "type": "instruction", // instruction | artifact | query | error
  "payload": {
    "task": "Generate API schema for User Auth",
    "context_refs": ["docs/auth_spec.md"]
  },
  "signature": "sha256_hash" // Security verification
}
```

## 3. The Registry
A dynamic lookup table defining agent capabilities.

```json
{
  "@roe/architect": {
    "capabilities": ["system_design", "mermaid_diagrams", "cloud_patterns"],
    "input_format": "text/markdown",
    "output_format": "text/markdown"
  },
  "@roe/backend": {
    "capabilities": ["python_fastapi", "sql_schema", "dockerfile"],
    "input_format": "spec/json",
    "output_format": "code/python"
  }
}
```

## 4. Shared Memory (Vector Store)
Instead of passing massive context windows, agents read/write to a shared **LanceDB** instance.

*   **Ingestion:** Project files are chunked and embedded automatically.
*   **Retrieval:** Agents query memory before acting.
    *   *Backend:* "Find existing User model definition." -> Retrieves `models.py`.

## 5. Orchestration Flow (Example: "Build a Todo App")

1.  **User:** "Build a Todo App."
2.  **Router (The Conductor):** Analyzes intent -> Assigns to **@roe/architect**.
3.  **@roe/architect:**
    *   Generates `SPEC.md` (Database schema, API endpoints).
    *   Publishes artifact to Bus.
    *   Sends instruction to **@roe/backend**: "Implement this schema."
4.  **@roe/backend:**
    *   Reads `SPEC.md`.
    *   Writes `main.py` and `models.py`.
    *   Runs unit tests (Executor).
    *   Reports: "API Ready."
5.  **@roe/frontend:**
    *   Reads `SPEC.md` and Backend report.
    *   Generates `App.tsx`.
6.  **Supervisor:** Detects completion -> Notifies User.

## 6. Implementation Stages

### Stage 1: The Mock Bus (v0.7.0 Alpha)
*   Simple Python `Queue`.
*   Manual routing logic in `omni.py`.
*   Agents are just prompts with different system instructions.

### Stage 2: The Vector Link (v0.7.1)
*   Integrate `lancedb`.
*   Auto-embed `omni_output/` files.

### Stage 3: The Autonomous Loop (v0.7.2)
*   Agents can self-correct (e.g., Backend fixes Frontend's API call errors).
