# How to Run Local Python AI on Mac Mini (Free)

**Stop paying for OpenAI API credits.**

In this guide, we will show you how to set up a fully offline, privacy-first Python coding assistant using **Omni** on your Mac Mini (M1/M2/M3).

## Prerequisites
- A Mac with Apple Silicon (M1 or newer).
- 8GB RAM (16GB recommended).
- 5 minutes.

## Step 1: Install Omni
Open your terminal and run:
```bash
curl -sL https://tinyurl.com/ai-omni | bash
```

## Step 2: Install the Python Cartridge
We don't use generic models. We use the **Aurelius Python Pro** cartridge, fine-tuned on high-quality Python 3.12 patterns.

```bash
omni install @aurelius/python-pro
```

## Step 3: Generate Code
Now you can ask Omni to write complex code.

```bash
omni run "Write a multi-threaded web scraper using aiohttp and beautifulsoup"
```

## Why this works better than GPT-4?
- **Zero Latency:** It runs on your device.
- **Privacy:** Your code never leaves your Mac.
- **Cost:** $0.

[Download Omni Now](https://github.com/AureliusSystemsAI/omni)
