#!/usr/bin/env python3
import time
from swarm.bus import OmniBus
from swarm.agent import SwarmAgent
from swarm.types import SwarmMessage, MessageType

# Mock LLM for testing the protocol flow
def mock_inference(system, user):
    if "architect" in system:
        return "Spec generated. @roe/backend: Create a User model with ID and Name."
    if "backend" in system:
        return "```python\nclass User(Base): ...\n```\nDone. Database schema ready."
    return "I don't know."

def main():
    print("🐝 Initializing Omni Swarm v0.7.0 (Protocol Test)...")
    
    # 1. Setup Bus
    bus = OmniBus()
    
    # 2. Spawn Agents
    architect = SwarmAgent(
        name="@roe/architect", 
        bus=bus, 
        llm_client=mock_inference,
        system_prompt="You are @roe/architect. Design systems."
    )
    
    backend = SwarmAgent(
        name="@roe/backend", 
        bus=bus, 
        llm_client=mock_inference,
        system_prompt="You are @roe/backend. Write Python code."
    )
    
    # 3. Trigger
    print("\n🚀 Injecting User Request...")
    
    # Manually publish as "user"
    msg = SwarmMessage(
        sender="user",
        recipient="@roe/architect",
        type=MessageType.INSTRUCTION,
        payload={"task": "Build a Todo App"}
    )
    bus.publish(msg)
    
    # 4. In a real threaded system, we'd wait. 
    # Since our bus is synchronous (process_queue calls callbacks immediately),
    # the recursion happens instantly. 
    # NOTE: The mock_inference above doesn't parse the "please implement" command to trigger the next agent.
    # In a real agent, 'think' would parse the LLM output and call 'send'.
    
    print("\n✅ Test Complete.")

if __name__ == "__main__":
    main()
