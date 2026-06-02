import json
from silero_vad import load_silero_vad
from silero_vad import read_audio
from silero_vad import get_speech_timestamps

model = load_silero_vad()

wav = read_audio("input_audio/sample.wav")

speech_timestamps = get_speech_timestamps(
    wav,
    model,
    return_seconds=True
)

print(speech_timestamps)

with open("timestamps/sample_timestamps.json", "w") as f:
    json.dump(speech_timestamps, f, indent=4)

print("Timestamps saved successfully")