import psycopg2
import os
from postgresdb import pgconnect
import numpy as np
import ast

def runnerq():
    conn = pgconnect()
    cur = conn.cursor()
    cur.execute("""
    SELECT state_embedding FROM mental_states WHERE state_label = 'neutral';
    """)
    runner_query = cur.fetchone()[0]
    #print(runner_query) - removed we can do later. 
    conn.close()

    return runner_query

def triggerq():
    conn = pgconnect()
    cur = conn.cursor()
    cur.execute("""
    SELECT trigger_embedding, trigger_activity, song_identity, mental_load
        FROM trusic_triggers;
    """)
    allrows = cur.fetchall()
    conn.close()

    triggers = []
    for row in allrows:
        triggers.append({
            "embedding": row[0],
            "song_identity": row[1],
            "trigger_activity": row[2],
            "mental_load": row[3]
        })

    return triggers

def comparing(runner_query, triggers):
    q_vector = runner_query

    neighbors = []

    for trigger in triggers:
        q_vec = np.array(ast.literal_eval(q_vector), dtype=float)
        t_vec = np.array(ast.literal_eval(trigger["embedding"]), dtype=float)
        sim = np.dot(q_vec, t_vec) / (np.linalg.norm(q_vec) * np.linalg.norm(t_vec))
        song_identity = trigger["song_identity"]
        trigger_activity = trigger["trigger_activity"]
        mental_load = trigger["mental_load"]
        neighbors.append({
            "score": sim,
            "trigger_activity": trigger_activity,
            "song_identity": song_identity,
            "load": mental_load,
        })

    neighbors.sort(key=lambda x : x["score"], reverse=True)
    return neighbors[:3]

if __name__ == "__main__":
    queryv = runnerq()
    triggers = triggerq()
    neighbors = comparing(queryv, triggers)
    top_k = neighbors[:3]
    print(top_k)


