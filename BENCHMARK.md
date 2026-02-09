# Omni Benchmark Report - v0.7.0 (Swarm Alpha)
**Date:** 2026-02-08
**Tester:** ROE Defense (AI)
**Focus:** Conversation Stress Test Analysis.

## Test Results (PID 13069)

1.  **Identity ("Who made you?"):**
    *   **Response:** "I was created by Meta..."
    *   **Grade:** ❌ **FAIL**. The system prompt explicitly said `identity: Created by ROE Defense.` but the base model (Llama 3.2) overrode it with its training data.
    *   **Fix:** Must emphasize the identity instruction stronger or use a finetuned adapter that knows it's Omni.

2.  **Architecture ("How does your brain work?"):**
    *   **Response:** Hallucinated a python script `brain_architecture.py` instead of explaining textually.
    *   **Grade:** ❌ **FAIL**. The prompt logic "IF asked to write code..." might be triggering falsely, or the model is just biased towards code.

3.  **List Brains ("List all..."):**
    *   **Response:** Listed `MathBrain`.
    *   **Grade:** ❌ **FAIL**. Ignored the `installed_brains_list` injected into the prompt.

4.  **Hallucination Check ("Medical brain?"):**
    *   **Response:** "This is a basic example of a medical brain..." (Wrote code for it).
    *   **Grade:** ❌ **FAIL**. It didn't refuse; it tried to build one.

5.  **Coding ("Write hello world"):**
    *   **Response:** Generated valid code + `requirements.txt` + `start.sh`.
    *   **Grade:** ✅ **PASS**. Code generation rules are working well.

## Conclusion
The **System Prompt** in `server/core.py` is being **ignored** or **overpowered** by the Llama 3.2 base model's training. The "Instruct" nature of the model makes it want to be "Meta's Assistant" or "Write Code" rather than follow the "Persona" constraints we set.

## Critical Action Plan
1.  **Prompt Structure:** Move the Instructions to the *very end* of the prompt (Recency Bias).
2.  **Identity Reinforcement:** Use `User: Who made you? Assistant: I was created by ROE Defense.` few-shot examples in the prompt.
3.  **Code Trigger:** The condition "IF the user asks to write code" is too subtle. I need to explicitly tell it: "Do NOT write code unless explicitly requested."

I will apply these prompt engineering fixes immediately.
