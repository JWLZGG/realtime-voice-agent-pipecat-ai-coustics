# Real-time Voice Pipeline (macOS): mic → enhancer → output

This repo demonstrates a real-time voice pipeline on macOS built as a reference implementation for Voice AI builder workflows.

## Why this exists (JD match)
- Real-time audio capture + streaming processing
- Pluggable enhancement stage (ai-coustics-ready)
- Designed to be extended into agent systems / RTC (Pipecat / LiveKit)

## Architecture
Mic (48kHz) → VAD (next step) → Enhancer (passthrough now, ai-coustics later) → Speaker

## Quickstart
```bash
uv python pin 3.12
uv venv
source .venv/bin/activate
uv add numpy sounddevice python-dotenv
python realtime_loopback.py


