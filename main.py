#!/usr/bin/env python3
"""
Voice Recorder
Author: brainiacweb-tech
"""
import wave, os, datetime

def record(filename, duration, rate=44100, channels=1):
    try:
        import sounddevice as sd
        import numpy as np
    except ImportError:
        print("Install dependencies: pip install sounddevice numpy"); return
    print(f"Recording for {duration} seconds... (speak now)")
    audio = sd.rec(int(duration * rate), samplerate=rate, channels=channels, dtype='int16')
    sd.wait()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(audio.tobytes())
    size = os.path.getsize(filename)
    print(f"Saved: {filename} ({size:,} bytes)")

def play_back(filename):
    try:
        import sounddevice as sd
        import soundfile as sf
        data, rate = sf.read(filename)
        print(f"Playing: {filename}")
        sd.play(data, rate); sd.wait()
    except ImportError:
        print("Install soundfile: pip install soundfile")
    except Exception as e:
        print(f"Playback error: {e}")

if __name__ == "__main__":
    print("=" * 42)
    print("         Voice Recorder")
    print("=" * 42)
    while True:
        print("\n1. Record\n2. Play last recording\n3. Quit")
        choice = input("Choice: ").strip()
        if choice == "1":
            try:
                dur = int(input("Duration in seconds: "))
            except ValueError:
                dur = 5
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"recording_{ts}.wav"
            record(fname, dur)
        elif choice == "2":
            files = sorted(f for f in os.listdir('.') if f.endswith('.wav'))
            if files:
                play_back(files[-1])
            else:
                print("No recordings found.")
        elif choice == "3":
            break
