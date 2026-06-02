from pydub import AudioSegment
import os

input_folder = "DATASETS"
output_folder = "WAV_FILES"

os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    if file.endswith(".mp3"):

        mp3_path = os.path.join(input_folder, file)

        wav_name = os.path.splitext(file)[0] + ".wav"
        wav_path = os.path.join(output_folder, wav_name)

        audio = AudioSegment.from_mp3(mp3_path)

        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)

        audio.export(wav_path, format="wav")

        print(f"Converted: {file}")

print("All files converted successfully!")