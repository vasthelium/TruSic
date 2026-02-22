# Nearest neighbors - learn via memory
# also adding HF embeddings to learn via represenations. without tuning the HF models. 
# k-NN teaches : distance, similarities, neighborhoods in patterns, data etc. 
import os
from huggingface_hub import InferenceClient
import shutil
from postgresdb import pgconnect, init_db, create_tables, insert_trigger, insert_mentalstates

HF_TOKEN = os.getenv("HF_Token")

def read_triggers():
    trigger_file = "/Users/hussain/Obsidian Vault/ProJect Trusic/musictriggers.md"
    
    if os.path.exists(trigger_file):
        with open(trigger_file, "r") as f:
            content = f.read()
            blocks = [b.strip() for b in content.split('---') if b.strip()]
            pending_trigger_activities = []
            pending_triggers = []

            for block in blocks:
                trigger = {}
                for line in block.splitlines():
                    if ":" in line:
                        key, value = line.split(":", 1)
                        trigger[(key.strip())] = value.strip()
                if trigger.get("processed") == "false":
                    pending_triggers.append(trigger)
                    pending_trigger_activities.append(trigger["trigger_activity"])
            return pending_triggers, pending_trigger_activities
        
def states():
    state_levels = ["settled", "focused", "strained", "drifting", "overloaded", "restless", "grounded", "neutral"]
    return state_levels

def send_to_hf(pending_trigger_activities, state_levels):
    client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN,
    )

    embeddings = client.feature_extraction(
    pending_trigger_activities,
    model="BAAI/bge-small-en-v1.5",
    )
    state_embeddings = client.feature_extraction(
    state_levels,
    model="BAAI/bge-small-en-v1.5",
    )
    # print(len(embeddings), len(embeddings[0])) sanity first
    return embeddings, state_embeddings

def pair_triggers(triggers, embeddings): 
    paired = []

    for i in range(len(embeddings)):
        trigger = triggers[i]
        embedding = embeddings[i].tolist()

        trigger["embedding"] = embedding
        paired.append(trigger)

    return paired

def senddb(paired, state_embeddings, state_levels):
    conn = pgconnect()
    init_db(conn)
    create_tables(conn)
    for trigger in paired:
        insert_trigger(conn, trigger)

    for i in range(len(state_embeddings)):
        insert_mentalstates(conn, {"state_label": state_levels[i], "state_embedding": state_embeddings[i].tolist()})
    conn.close()

if __name__ == "__main__":
    pending_triggers, pending_trigger_activities = read_triggers()
    state_levels = states()
    trigger_embeddings, state_embeddings = send_to_hf(pending_trigger_activities, state_levels)
    paired = pair_triggers(pending_triggers, trigger_embeddings)
    senddb(paired, state_embeddings, state_levels)




