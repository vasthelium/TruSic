from app.db.db_repository import (
pgconnect, init_db, create_audiotriggers_tables,
insert_audiotriggers, read_audio_triggers, connection_pool)

def sendaudiotodb(embedded_f):
    conn = pgconnect()
    try:
        init_db(conn)
        create_audiotriggers_tables(conn)
        for audiotriggers in embedded_f:
            insert_audiotriggers(conn, 
            {
            "type": "trusic_audio_observation",
            "song_identity": audiotriggers["filename"],
            "trigger_embedding": audiotriggers["embedded_vector"][0].tolist()
            }
        )
            print(f"Inserted: {audiotriggers['filename']}")
        conn.commit()
    finally:
        connection_pool.putconn(conn)
    print("DB write complete.")

def read_songdata():
    conn = pgconnect()
    try:
        song_data= read_audio_triggers(conn)
    finally:
        connection_pool.putconn(conn)
    return song_data