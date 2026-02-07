# Training Protocol: The Path to Sovereignty

## Dataset Scaling Targets (Samples)

Based on LIMA (Less Is More) and LoRA scaling laws for 1B/3B models.

| Tier | Status | 1B (Specialist) | 3B (Agent) | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **MVP** | ✅ **LIVE** | 500 | 1,000 | "It Works." Basic syntax and pattern recognition. |
| **Production** | 🚧 **NEXT** | 2,500 | 5,000 | "Reliable." Handles edge cases and complex logic. |
| **Sovereign** | 🔮 **GOAL** | 10,000 | 15,000 | "Perfection." Deep reasoning, zero hallucinations. |

## Quality > Quantity
- **Format:** Chain-of-Thought (CoT) is mandatory for 3B brains.
- **Diversity:** Samples must cover "How to X", "Fix Y", "Explain Z", and "Refactor Q".
- **Validation:** Every sample must pass a syntax check before training.

## The Training Loop
1.  **Generate:** `synth_gen.py` creates raw JSONL.
2.  **Validate:** `supervisor.py` checks syntax (mock execution).
3.  **Train:** `mlx_lm.lora` runs for 600-1000 iterations.
4.  **Fuse:** Merge adapter into base model.
5.  **Benchmark:** Verify improvement against previous version.
