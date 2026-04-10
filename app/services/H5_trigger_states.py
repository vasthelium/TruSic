import os
import shutil
from app.services.A2_privacy_killswitch import privacy_switch
from app.services.A3_classify import classify
from app.db.db_service_human import read_ouradata
from app.db.db_service_audio import read_songdata
from huggingface_hub import InferenceClient
from app.ml.models.Learn import newmlp
import numpy as np

#config
HF_TOKEN = os.getenv("HF_Token")

#mental_state derivation
def healthstat():
    oura_data = read_ouradata()
    #Derive the needed OURA data
    day = oura_data["day"]
    # sleep_score = oura_data["sleep_score"]
    total_sleep_duration = oura_data["total_sleep_duration"]/3600
    average_hrv = oura_data["average_hrv"]
    resting_heart_rate = oura_data["resting_heart_rate"]
    readiness_score = oura_data["readiness_score"]

    #mock Steps #baselined 9000
    steps = 9000
    baseline_hrv = 60
    hrv_balance = average_hrv / baseline_hrv
    cognitive_state = (readiness_score * hrv_balance) / steps

    return cognitive_state

#triggers from file
def read_triggers():
    trigger_file = "data/trusic_triggers.md"
    
    if os.path.exists(trigger_file):
        with open(trigger_file, "r") as f:
            content = f.read()
            blocks = [b.strip() for b in content.split('---') if b.strip()]
            music_triggers = []

            for block in blocks:
                trigger = {}
                for line in block.splitlines():
                    if ":" in line:
                        key, value = line.split(":", 1)
                        trigger[(key.strip())] = value.strip()
                music_triggers.append(trigger)
            return music_triggers
        
def audioname():
    song_data= read_songdata()
    song_name_list = []

    for data in song_data:
        song_name_list.append({
            "song_name": data[0]
            })
    return song_name_list

def file_compare(music_triggers, song_name_list):

    song_set = set(item["song_name"].rsplit(".", 1)[0] for item in song_name_list)
    final_meta = []

    for metatriggers in music_triggers:
        type = metatriggers["type"]
        song_identity = metatriggers["song_identity"]
        trigger_activity = metatriggers["trigger_activity"]
        trigger_drive = metatriggers["trigger_drive"]
        if song_identity in song_set:
            final_meta.append({
                "type": type,
                "song_identity": song_identity,
                "trigger_activity": trigger_activity,
                "trigger_drive": trigger_drive,
                })
    return final_meta

def create_features():
    music_triggers = read_triggers()
    song_name_list = audioname()
    metaitems = file_compare(music_triggers, song_name_list)
    cognitive_state = healthstat()

    features_list = []

    for items in metaitems:
        features_list.append({
            "type": items["type"],
            "song_identity": items["song_identity"],
            "trigger_activity": items["trigger_activity"],
            "trigger_drive": items["trigger_drive"],
            "cognitive_state":cognitive_state
        })

    return features_list

def send_to_hf(features_list):

    trigger_activities = []

    for items in features_list:
        trigger_activities.append(items["trigger_activity"])

    client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN,
    )

    triggeract_embeddings = client.feature_extraction(
    trigger_activities,
    model="BAAI/bge-small-en-v1.5",
    )
    
    # print(len(embeddings), len(embeddings[0])) sanity first
    return triggeract_embeddings

def numerical_features():
    features_list = create_features()
    drive_lookup = {
        "emotion": 2,
        "neutral": 1,
        "cognition": 0
    }
    numericaltoMLP = []
    embeddings = send_to_hf(features_list)
    cognitive_state = healthstat()

    for index, items in enumerate(features_list):
        trigger_drive = drive_lookup[items["trigger_drive"]]
        type = items["type"]
        song_identity = items["song_identity"]
        trigger_activity =  items["trigger_activity"]
        embedding = embeddings[index]
        numericaltoMLP.append({
            "cognitive_state": cognitive_state,
            "trigger_drive": trigger_drive,
            "embedding": embedding.tolist()
        })
    return numericaltoMLP

def mlpfunc(numericaltoMLP: dict):
    send_to_mlp = []

    for numericals in numericaltoMLP:
        send_to_mlp.append([numericals["cognitive_state"], numericals["trigger_drive"]] +  numericals["embedding"])
    return send_to_mlp

# ML chapter reading. - skimmed

def mlp():
    numeric_features = numerical_features()
    incoming_vec = mlpfunc(numeric_features)

    newvec = np.array(incoming_vec)
    np.random.seed(42) # seeding so same random weight every run
    W1 = np.random.randn(386, 256) #random is a module, randn is a function of random / random is a module of numpy
    b1 = np.zeros(256) #zeroes function of numpy # bias start neutral

    W2 = np.random.randn(256, 512)
    b2 = np.zeros(512)

    x = newvec #input matrix created
    Z = np.dot(x, W1) + b1 
    #Z = x @ W1 + b1 aslo same as above line

    #concept activation A = max(0, Z) - negative 0, positives stays Z ADDS NON LINEARITY - **VERY IMPORTANT**
    A1 = np.maximum(0, Z)
    #now push to 512 dims
    Z2 = np.dot(A1, W2) + b2
    Z2 = Z2 / (np.linalg.norm(Z2, axis=1, keepdims=True) + 1e-8) #Normalization (specifically L2 normalization)
    # each value in row / that row’s length so each row becomes unit vector (length = 1)
    # 1e-8 is a small number no impact on real values / it prevents divide by zero

    return Z2

def pair_statetriggers(features_list, Z2):
    statetriggers = [] 

    for i in range(len(Z2)):
        item = features_list[i]
        finaltrigdict = {
            "type": item["type"],
            "song_identity": item["song_identity"],
            "trigger_activity":item["trigger_activity"],
            "trigger_drive": item["trigger_drive"],
            "stateembedding": Z2[i].tolist()
        }
        statetriggers.append(finaltrigdict)
    return statetriggers

def build_statetriggers():
    features_list = create_features()
    Z2 = newmlp()
    statetriggers = pair_statetriggers(features_list, Z2)
    return statetriggers


    



