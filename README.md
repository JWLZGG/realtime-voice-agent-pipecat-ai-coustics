# Real-time Voice Pipeline (macOS): mic → enhancer → output

This repository demonstrates a real-time voice pipeline on macOS, built as a reference implementation for Voice AI builder workflows.

It focuses on live audio capture, streaming pipelines, and transport lifecycle correctness, rather than offline batch processing.

## Why this exists 
This project was built to explicitly exercise and demonstrate:

- Real-time audio capture and streaming processing

- Hands-on Voice AI builder experience (mic → frames → pipeline → output)

- A pluggable enhancement stage (passthrough now, ai-coustics integration next)

- Integration patterns for agent systems / RTC stacks
(Pipecat today, LiveKit / telephony stacks next)

It is intentionally minimal but realistic, surfacing the same problems developers hit when building real-time voice systems.

## Architecture
Microphone (48 kHz)
    ↓
Local Audio Transport
    ↓
Pipecat Pipeline
    ↓
[ Enhancement Stage ]
    (currently passthrough,
     ai-coustics streaming-ready)
    ↓
Local Audio Output (speakers)

Key characteristics:

- Single-process, low-latency loopback

- Explicit sample-rate handling (48 kHz)

- Designed so transports, processors, and enhancers can be swapped independently

## What this pipeline does

At runtime, the pipeline:

- Captures live microphone audio using a local transport

- Converts raw audio into Pipecat frames

- Streams frames through a Pipecat pipeline

- Applies an enhancement stage (currently a passthrough placeholder)

- Outputs processed audio back to the system speakers

This mirrors the structure used in real Voice AI systems, where enhancement, transcription, or agent logic sits between input and output.

## Why a “bridge” / adapter layer exists

One of the core learnings in this project is that real-time audio systems are strict about lifecycle and frame contracts.

In practice:

Audio transports emit chunks of audio

Pipecat pipelines expect specific frame types, in a strict order

The pipeline must be started exactly once, and shut down cleanly

The adapter / bridge layer exists to:

Translate transport audio into the exact Pipecat frame types the pipeline expects

Enforce correct start / run / stop semantics

Prevent invalid audio frames from entering the pipeline before it is ready

Make it easy to swap transports (mic, WebRTC, file, telephony) without rewriting the pipeline

This pattern is essential when building production Voice AI systems.

## The problem I hit (and how I fixed it)
The issue

While iterating on the pipeline, I ran into a classic real-time Voice AI failure mode:

An error occurred mid-run

The audio loop continued running in the background

Subsequent runs behaved unpredictably

The pipeline reported frame-ordering / lifecycle errors

This is a very common problem when working with real-time audio and async pipelines.

## Root cause

Two underlying issues:

Lifecycle management
The pipeline runner and transport must be started and stopped cleanly. If an exception occurs and the old runner is not cancelled, the “error flow” can continue running invisibly.

Frame contract enforcement
Pipecat enforces strict rules about when audio frames may be processed. Sending audio before the pipeline is fully started (or after it should have stopped) correctly triggers errors.

## The fix

I resolved this by:

Ensuring there is exactly one active runner/task at a time

Explicitly killing previous error flows during development

Constructing the entire pipeline before starting the runner

Centralising audio frame translation in a single adapter layer

After that, the pipeline starts cleanly, runs deterministically, and shuts down correctly.

## Why this matters (developer experience)

These are exactly the issues developers hit when they first work with real-time Voice AI:

“Why is my stream still running after an error?”

“Why does my audio pipeline fail even though the code looks correct?”

“Why does frame ordering matter so much?”

This repo acts as a reference implementation showing:

Correct real-time audio lifecycle handling

A clean transport → pipeline → processing separation

A practical foundation for integrating ai-coustics streaming, RTC, or agent systems

## Quickstart
```bash
uv python pin 3.12
uv venv
source .venv/bin/activate
uv add numpy sounddevice python-dotenv
python realtime_loopback.py


