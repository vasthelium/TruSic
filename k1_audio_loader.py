import os
import numpy as np
import librosa
import torch
import torchaudio

def load_audio():
    audio_files = "/Users/hussain/raw_soundfiles"
    # print("Path exists?", os.path.exists(audio_files))#debug line
    towave = [] 

    for file in os.listdir(audio_files):
        # print("found file?:", file) - debug line
        if file.endswith(".m4a"):
            audio_path = os.path.join(audio_files, file)
            y, sr = librosa.load(audio_path, sr=16000, mono=True)

            y_tensor = torch.tensor(y, dtype=torch.float32)
            y_tensor = y_tensor.unsqueeze(0)
            towave.append({
                "file_name": file,
                "wave_form":y,
                "tensor" : y_tensor,
                "sample_rate": sr,
                })
    for item in towave:
        print(
            item["file_name"],
            item["tensor"].shape,
            item["sample_rate"]
            )
    return towave
    # print(file, y_tensor.shape, sr)#debug line

if __name__ == "__main__":
    load_audio()
    




