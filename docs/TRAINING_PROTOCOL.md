# Cartridge Training Strategy

## The "Zero Trace" Protocol (User-Side Training)

Omni allows users to fine-tune custom cartridges (`@roe/custom`) from their own documents. To maintain security, we strictly manage the lifecycle of training data.

### Workflow

1.  **Ingest:** User points Omni to a folder (`/docs`).
2.  **Synthesize:** Omni (using the local LLM) generates Question-Answer pairs from the documents.
    *   *Artifact:* `~/.omni/temp/training_data.jsonl` (Plaintext! Dangerous!)
3.  **Train:** `mlx` or `llama.cpp` runs the LoRA fine-tuning.
    *   *Artifact:* `~/.omni/models/adapters/custom_lora.gguf`
4.  **Sanitize (The Feature):**
    *   Immediately after training success, the system performs a secure delete (`shred -u` or overwrite) on `training_data.jsonl`.
    *   The original user documents are touched/read-only.

### Implementation Plan

- [ ] Create `train_cartridge.py` (The local training orchestrator).
- [ ] Add `cleanup_artifacts()` function to secure-delete intermediate JSONL.
- [ ] Expose via CLI: `omni learn ./my-docs --name "project-x"`

### Internal Note (ROE Defense)
For our *internal* factory (`synth_gen.py`), we keep the datasets for now to debug quality. But we should apply this same logic to the *release* version of the software.
