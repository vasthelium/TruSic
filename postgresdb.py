import psycopg2
import os

def pgconnect():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise ValueError("DB URL not set in this terminal")
    return psycopg2.connect(dsn)

def init_db(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE EXTENSION IF NOT EXISTS vector;
    """)
    conn.commit()

def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS trusic_triggers (
        id SERIAL PRIMARY KEY,                 
        created_at TIMESTAMPTZ DEFAULT now(),  
        type TEXT,                             
        song_identity TEXT,
        trigger_activity TEXT,                 
        trigger_type TEXT,
        trigger_drive TEXT,
        mental_load TEXT,                      
        trigger_embedding vector(384),         
        processed BOOLEAN DEFAULT false
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS mental_states (
        id SERIAL PRIMARY KEY,  
        state_label TEXT,                             
        state_embedding vector(384)
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS trusic_audiotriggers (
        id SERIAL PRIMARY KEY,                 
        created_at TIMESTAMPTZ DEFAULT now(),  
        type TEXT,                             
        song_identity TEXT,
        trigger_activity TEXT,                 
        trigger_type TEXT,
        trigger_drive TEXT,                      
        trigger_embedding vector(512)         
    )
    """)
    print("Tables ensured.")
    conn.commit()

def insert_trigger(conn, trigger):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO trusic_triggers (
            type,
            song_identity,
            trigger_activity,
            trigger_type,
            trigger_drive,
            mental_load,
            trigger_embedding,
            processed
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        trigger["type"],
        trigger["song_identity"],
        trigger["trigger_activity"],        
        trigger["trigger_type"],
        trigger["trigger_drive"],
        trigger["mental_load"],
        trigger["embedding"],          
        True                            # Marked processed on Insert
    ))

    trigger_id = cur.fetchone()[0]
    conn.commit()
    return trigger_id

def insert_mentalstates(conn, state):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO mental_states(
            state_label,
            state_embedding
        )
        VALUES (%s, %s)
        RETURNING id;
    """, (
        state["state_label"],
        state["state_embedding"]        
    ))

    state_id = cur.fetchone()[0]
    conn.commit()
    return state_id

def insert_audiotriggers(conn, audiotriggers):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO trusic_audiotriggers (
            type,
            song_identity,
            trigger_activity,
            trigger_type,
            trigger_drive,
            trigger_embedding
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        audiotriggers["type"],
        audiotriggers["song_identity"],
        audiotriggers["trigger_activity"],        
        audiotriggers["trigger_type"],
        audiotriggers["trigger_drive"],
        audiotriggers["embedded_vec"],         
    ))

    audiotrigger_id = cur.fetchone()[0]
    conn.commit()
    return audiotrigger_id

