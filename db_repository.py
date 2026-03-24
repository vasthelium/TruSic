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

def create_audiotriggers_tables(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS trusic_audio_triggers (
        id SERIAL PRIMARY KEY,                 
        created_at TIMESTAMPTZ DEFAULT now(),  
        type TEXT,                             
        song_identity TEXT,                                  
        trigger_embedding vector(512)         
        )
    """)
    print("Tables ensured.")
    conn.commit()

def insert_audiotriggers(conn, audiotriggers):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO trusic_audio_triggers (
            type,
            song_identity,
            trigger_embedding
        )
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (
        audiotriggers["type"],
        audiotriggers["song_identity"],      
        audiotriggers["trigger_embedding"]         
    ))
    audiotrigger_id = cur.fetchone()[0]
  
    return audiotrigger_id

def create_ouradaily_table(conn):
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS oura_daily_data (
        id TEXT PRIMARY KEY,
        day DATE,
        average_heart_rate DOUBLE PRECISION,
        average_hrv DOUBLE PRECISION,
        hrv_interval DOUBLE PRECISION,
        deep_sleep_duration DOUBLE PRECISION,
        light_sleep_duration DOUBLE PRECISION,
        rem_sleep_duration DOUBLE PRECISION,
        total_sleep_duration DOUBLE PRECISION,
        body_temperature DOUBLE PRECISION,
        resting_heart_rate DOUBLE PRECISION,
        hrv_balance DOUBLE PRECISION,
        sleep_balance DOUBLE PRECISION,
        sleep_regularity DOUBLE PRECISION,
        readiness_score DOUBLE PRECISION     
                )           
        """)
    conn.commit()
    
def insert_ouradaily(conn, flat_data):
    cur = conn.cursor()

    for data in flat_data:
        cur.execute(
            """
            INSERT INTO oura_daily_data (
                id,
                day,
                average_heart_rate,
                average_hrv,
                hrv_interval,
                deep_sleep_duration,
                light_sleep_duration,
                rem_sleep_duration,
                total_sleep_duration,
                body_temperature,
                resting_heart_rate,
                hrv_balance,
                sleep_balance,
                sleep_regularity,
                readiness_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING         
            """, 
            (
                data["id"],
                data["day"],
                data["average_heart_rate"],
                data["average_hrv"],
                data["hrv_interval"],
                data["deep_sleep_duration"],
                data["light_sleep_duration"],
                data["rem_sleep_duration"],
                data["total_sleep_duration"],
                data["body_temperature"],
                data["resting_heart_rate"],
                data["hrv_balance"],
                data["sleep_balance"],
                data["sleep_regularity"],
                data["readiness_score"]
            )
        )

def read_oura_daily_data(conn):
    curs = conn.cursor()
    curs.execute("""
            SELECT day, readiness_score,
            total_sleep_duration, average_hrv,
            resting_heart_rate
            FROM oura_daily_data
            ORDER BY day DESC
            LIMIT 1
        """
        )
    row = curs.fetchone()
    if not row:
        return None
    return{
        "day": row[0],
        "readiness_score": row[1],
        "total_sleep_duration": row[2],
        "average_hrv": row[3],
        "resting_heart_rate": row[4]
        }

def read_audio_triggers(conn):
    curs = conn.cursor()
    curs.execute("""
            SELECT song_identity
            FROM trusic_audio_triggers
            ORDER BY created_at DESC
        """
        )
    row = curs.fetchall()
    if not row:
        return None
    return row
    
def create_state_trigger_table(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS trusicstate_triggers (
        id SERIAL PRIMARY KEY,                 
        created_at TIMESTAMPTZ DEFAULT now(),  
        type TEXT,                             
        song_identity TEXT,
        trigger_activity TEXT,                 
        trigger_drive TEXT,                     
        stateembedding vector(512)
    )
    """)
    print("Tables ensured.")
    conn.commit()

def insert_state_triggers(conn, state_triggers):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO trusicstate_triggers (
            type,
            song_identity,
            trigger_activity,
            trigger_drive,
            stateembedding
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        state_triggers["type"],
        state_triggers["song_identity"],
        state_triggers["trigger_activity"],        
        state_triggers["trigger_drive"],
        state_triggers["stateembedding"]          
    ))
    state_trigger_id = cur.fetchone()[0]
    return state_trigger_id     