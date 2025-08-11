import math
import random
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 44100


def generate_hit(path: str) -> None:
    """Create a short sine wave beep used when the ball is hit."""
    freq = 880
    duration = 0.1
    samples = [
        struct.pack('<h', int(32767 * math.sin(2 * math.pi * freq * i / SAMPLE_RATE)))
        for i in range(int(SAMPLE_RATE * duration))
    ]
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(b''.join(samples))


def generate_applause(path: str) -> None:
    """Create a more realistic applause sound by layering short claps."""
    duration = 1.2
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # Generate many short clap noises at random times to emulate a crowd
    clap_length = int(0.05 * SAMPLE_RATE)
    for _ in range(60):
        start = random.randint(0, total_samples - clap_length)
        for i in range(clap_length):
            # Each clap is a decaying burst of noise
            envelope = math.exp(-40 * i / SAMPLE_RATE)
            samples[start + i] += random.uniform(-1, 1) * envelope

    # Normalize and convert to 16-bit PCM
    peak = max(abs(s) for s in samples) or 1
    frames = [struct.pack('<h', int(32767 * s / peak)) for s in samples]

    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(b''.join(frames))


if __name__ == '__main__':
    generate_hit('assets/hit.wav')
    generate_applause('assets/applause.wav')
