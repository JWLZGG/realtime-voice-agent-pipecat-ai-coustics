import os
import queue
import numpy as np
import sounddevice as sd
from dotenv import load_dotenv

from src.enhancers import get_enhancer

# Optional: ai-coustics SDK (only if you have a key)
try:
    from aic_sdk import AIC  # adjust later if needed
except Exception:
    AIC = None

load_dotenv()

SAMPLE_RATE = 48000
CHANNELS = 1
BLOCK_MS = 20
BLOCK = int(SAMPLE_RATE * (BLOCK_MS / 1000.0))

enhancer = get_enhancer()

q = queue.Queue()

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    x = indata[:, 0].copy()  # mono float32

    y = enhancer.process(x, SAMPLE_RATE)


    outdata[:] = y.reshape(-1, 1)

def main():
    print("Starting realtime mic loopback. Ctrl+C to stop.")
    with sd.Stream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        blocksize=BLOCK,
        dtype="float32",
        callback=callback,
    ):
        while True:
            sd.sleep(1000)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")

