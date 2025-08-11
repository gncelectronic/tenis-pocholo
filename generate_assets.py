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
    """Create a burst of white noise used for the applause sound."""
    duration = 0.5
    samples = [
        struct.pack('<h', int(32767 * random.uniform(-1, 1)))
        for _ in range(int(SAMPLE_RATE * duration))
    ]
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(b''.join(samples))


if __name__ == '__main__':
    generate_hit('assets/hit.wav')
    generate_applause('assets/applause.wav')
