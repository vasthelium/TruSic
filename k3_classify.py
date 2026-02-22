from k2_privacy_killswitch import privacy_switch
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

def classify():
    safe_files, speech_files = privacy_switch() #inside classify called, privacy_switch
    incoming_files = safe_files
    classification_files = []
    model = hub.load("https://tfhub.dev/google/yamnet/1")
    class_map = model.class_map_path().numpy()
    class_names = [line.split(",")[2].strip() for line in open(class_map).read().splitlines()]
    allowed_list = [
    "Music",
    "Musical instrument",
    "Plucked string instrument",
    "Guitar",
    "Bass guitar",
    "Piano",
    "Keyboard (musical)",
    "Drum",
    "Drum machine",
    "Percussion",
                    ]
    for items in incoming_files:
        file_name = items["file_name"]
        waveform = items["wave_form"]   # extracted waveform
        sample_rate = items["sample_rate"]       
        y = waveform.astype(np.float32)    #casted to float 32
        ytf = tf.convert_to_tensor(y)      #converted to TF tensor here
        score, embeddings, spectogram = model(ytf)
        avg_scores = tf.reduce_mean(score, axis=0) #temporal pooling or aggregation across time
        st_indx = int(tf.argmax(avg_scores, axis=0).numpy())
        predicted_label = class_names[st_indx]
        top5 = tf.argsort(avg_scores, direction="DESCENDING")[:5]
        
        top5_labels = [class_names[int(idx.numpy())] for idx in top5]
        if any(label in allowed_list for label in top5_labels):
            classification_files.append({
            "file_name": file_name,
            "predicted_label": predicted_label,
            "waveform": waveform,
            "sample_rate": sample_rate
            })
            print(f"{file_name} → {predicted_label}")

    return classification_files

if __name__ == "__main__":
    results = classify()
