from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch

def privacy_switch(audio_data):

    idenify = []
    model_w = "facebook/wav2vec2-base-960h"
    model = Wav2Vec2ForCTC.from_pretrained(model_w)
    model.eval()
    processor = Wav2Vec2Processor.from_pretrained(model_w)
    safe_files = []
    speech_files = []
    for item in audio_data:
        tensor = item["tensor"]
        sample_rate = item["sample_rate"]
        file_name = item["file_name"]
        waveform = item["wave_form"]
        idenify.append({
            "tensor": tensor,
            "sample_rate": sample_rate,
            "file_name": file_name,
            "waveform": waveform
        })
        input_features = processor(
            waveform,
            sampling_rate = sample_rate,
            return_tensors ="pt")
        outputs = model(**input_features)
        logits = outputs.logits
        predicted_token_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_token_ids)
        # print(transcription) debug line
        text = transcription[0].strip()

        if len(text) > 5:
            speech_files.append(item)
            print(f"Speech detected in {file_name}: {text}")
        else:
            safe_files.append(item)
            print(f"no speech in {file_name}")

    return safe_files, speech_files
    