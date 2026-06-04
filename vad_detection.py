import os
import json
import soundfile as sf

from silero_vad import (
    load_silero_vad,
    read_audio,
    get_speech_timestamps
)

# =====================================================
# PATHS
# =====================================================

AUDIO_DIR = "audio"
TIMESTAMP_DIR = "timestamps"
SEGMENT_DIR = "output segments"

SAMPLE_RATE = 16000

# =====================================================
# CREATE OUTPUT FOLDERS
# =====================================================

os.makedirs(TIMESTAMP_DIR, exist_ok=True)
os.makedirs(SEGMENT_DIR, exist_ok=True)

# =====================================================
# LOAD MODEL
# =====================================================

print("Loading Silero VAD...")

model = load_silero_vad()

print("Model loaded.\n")

# =====================================================
# FIND AUDIO FILES
# =====================================================

audio_files = sorted(
    [
        f for f in os.listdir(AUDIO_DIR)
        if f.lower().endswith(".wav")
    ]
)

print(f"Found {len(audio_files)} WAV files.\n")

# =====================================================
# PROCESS EACH FILE
# =====================================================

for audio_file in audio_files:

    try:

        audio_path = os.path.join(
            AUDIO_DIR,
            audio_file
        )

        file_id = os.path.splitext(audio_file)[0]

        print(f"Processing: {audio_file}")

        # -----------------------------------------
        # LOAD AUDIO
        # -----------------------------------------

        wav = read_audio(
            audio_path,
            sampling_rate=SAMPLE_RATE
        )

        # -----------------------------------------
        # GET SPEECH TIMESTAMPS
        # -----------------------------------------

        speech_timestamps = get_speech_timestamps(
            wav,
            model,
            sampling_rate=SAMPLE_RATE,
            threshold=0.5,
            min_speech_duration_ms=250,
            min_silence_duration_ms=200,
            speech_pad_ms=100,
            return_seconds=True
        )

        # -----------------------------------------
        # SAVE JSON
        # -----------------------------------------

        json_path = os.path.join(
            TIMESTAMP_DIR,
            f"{file_id}.json"
        )

        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                speech_timestamps,
                f,
                indent=4
            )

        # -----------------------------------------
        # EXPORT SEGMENTS
        # -----------------------------------------

        sample_timestamps = get_speech_timestamps(
            wav,
            model,
            sampling_rate=SAMPLE_RATE,
            threshold=0.5,
            min_speech_duration_ms=250,
            min_silence_duration_ms=200,
            speech_pad_ms=100,
            return_seconds=False
        )

        file_segment_dir = os.path.join(
            SEGMENT_DIR,
            file_id
        )

        os.makedirs(
            file_segment_dir,
            exist_ok=True
        )

        for idx, segment in enumerate(sample_timestamps):

            start = segment["start"]
            end = segment["end"]

            segment_audio = wav[start:end]

            output_path = os.path.join(
                file_segment_dir,
                f"segment_{idx+1}.wav"
            )

            sf.write(
                output_path,
                segment_audio.numpy(),
                SAMPLE_RATE
            )

        print(
            f"✓ Saved timestamps and "
            f"{len(sample_timestamps)} segments"
        )

    except Exception as e:

        print(
            f"✗ Error processing "
            f"{audio_file}: {e}"
        )

print("\nDone.")