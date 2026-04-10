from app.db.db_repository import pgconnect
#from H5_trigger_states import mlp
from Learn import newmlp
import numpy as np

def trusic_NN():
    mlpvec = newmlp()
    conn = pgconnect()
    cur = conn.cursor()

    similar = []
    try:
        for vecs in mlpvec:
            cur.execute("""
                SELECT song_identity,
                    trigger_embedding <-> %s::vector AS distance
                    FROM trusic_audio_triggers
                    ORDER BY trigger_embedding <-> %s::vector
                    LIMIT 2;
                    """, (vecs.tolist(), vecs.tolist()))
            rows = cur.fetchall()
            for row in rows:
                similar.append({
                    "song_identity": row[0],
                    "score": row[1]
                })
    finally:
        conn.close()
    print(similar)
    return similar
# vector similarity search is the ::vector - relearn 

