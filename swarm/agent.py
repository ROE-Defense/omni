from typing import Dict, Any
from .types import SwarmMessage, MessageType
from .bus import OmniBus
from .memory import SwarmMemory # v0.7.1 Integration
import time

class SwarmAgent:
    def __init__(self, name: str, bus: OmniBus, llm_client=None, system_prompt: str = ""):
        self.name = name
        self.bus = bus
        self.llm_client = llm_client 
        self.system_prompt = system_prompt
        self.memory = SwarmMemory() # Shared Vector Store
        
        # Subscribe to bus
        self.bus.subscribe(self.name, self.on_message)

    def on_message(self, msg: SwarmMessage):
        """Handle incoming message."""
        # Don't react to own messages or artifacts (unless tasked to review)
        if msg.sender == self.name: return
        
        print(f"🤖 {self.name} received: {msg.type.value} from {msg.sender}")
        
        # Determine reaction
        if msg.type == MessageType.INSTRUCTION:
            self.think(msg)

    def think(self, trigger_msg: SwarmMessage):
        """Query the LLM and respond."""
        if not self.llm_client:
            print(f"⚠️ {self.name} has no brain (LLM client missing).")
            return

        user_content = trigger_msg.payload.get("task", str(trigger_msg.payload))

        # 1. RECALL: Check memory for relevant context
        print(f"🧠 {self.name} recalling...")
        context_docs = self.memory.search(user_content, limit=2)
        context_str = "\n".join([f"- {d['text']} (Source: {d['agent']})" for d in context_docs])
        
        full_context = f"Message from {trigger_msg.sender}:\n{user_content}\n\nRelevant Shared Memory:\n{context_str}"
        
        # 2. GENERATE: Call LLM
        response_text = self.llm_client(self.system_prompt, full_context)
        
        # 3. SAVE: Store the result in memory
        self.memory.add(response_text, self.name, metadata={"trigger": trigger_msg.id})
        
        # 4. ACT: Parse Response for Handoffs
        import re
        handoff = re.search(r'(@roe/[\w-]+):\s*(.*)', response_text, re.DOTALL)
        
        if handoff:
            recipient = handoff.group(1)
            content = handoff.group(2).strip()
            print(f"🔄 {self.name} -> {recipient}: Handoff initiated.")
            self.send(recipient, {"task": content})
        else:
            # Default Reply
            reply = SwarmMessage(
                sender=self.name,
                recipient=trigger_msg.sender,
                type=MessageType.ARTIFACT,
                payload={"content": response_text}
            )
            self.bus.publish(reply)

    def send(self, recipient: str, payload: Dict[str, Any]):
        msg = SwarmMessage(
            sender=self.name,
            recipient=recipient,
            type=MessageType.INSTRUCTION,
            payload=payload
        )
        self.bus.publish(msg)
