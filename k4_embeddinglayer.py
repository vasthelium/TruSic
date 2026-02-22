# Goal:Convert filtered music audio into vector embeddings to later perform similarity search (pgvector).
import torch
import torchaudio
import transformers
from transformers import ClapModel, ClapProcessor
import pytest
from k3_classify import classify
import numpy as np
from postgresdb import pgconnect, init_db, create_tables, insert_audiotriggers

def device():
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    return device

def embed(device):
    incoming = classify()
    hf_modelt = "laion/clap-htsat-unfused"
    model = ClapModel.from_pretrained(hf_modelt)
    model.to(device)
    model.eval()
    processor = ClapProcessor.from_pretrained(hf_modelt)

    embedded_f = []

    for items in incoming:
        file_name = items["file_name"]
        waveform = items["waveform"]
        sample_rate = items["sample_rate"]
        wave_tensor = torch.tensor(waveform, dtype=torch.float32) #needed for resampling with torch
        if sample_rate!= 48000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=48000)
            wave_tensor = resampler(wave_tensor)
        input_features = processor(
            audio=wave_tensor,
            sampling_rate = 48000,
            return_tensors = "pt")
        # input_features.to(device) replaced to below - relearn 
        input_features = {k: v.to(device) for k, v in input_features.items()}
        
        with torch.no_grad():
            embeddings = model.get_audio_features(**input_features).pooler_output

        l2embed = embeddings / torch.norm(embeddings, p=2, dim=-1, keepdim=True)

        embedv_normal = l2embed.detach().cpu()
        embedded_f.append(
            {
            "filename": file_name,
            "embedded_vector": embedv_normal,
            "sample_rate": sample_rate
            })
        print(f"{file_name} → embedding_dim: {embedv_normal.shape[-1]}")
    return embedded_f

def sendtodb(embedded_f):
    conn = pgconnect()
    init_db(conn)
    create_tables(conn)
    for audiotriggers in embedded_f:
        insert_audiotriggers(conn, 
        {
            "type": "trusic_audio_observation",
            "song_identity": audiotriggers["filename"],
            "trigger_activity": None,
            "trigger_type": None,
            "trigger_drive": None,
            "embedded_vec": audiotriggers["embedded_vector"][0].tolist()
        }
        )
        print(f"Inserted: {audiotriggers['filename']}")
    conn.close()
    print("DB write complete.")
 

if __name__ == "__main__":
    dev = device()
    results = embed(dev)
    sendtodb(results)


