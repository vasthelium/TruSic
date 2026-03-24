from db_repository import (
pgconnect, init_db,
create_ouradaily_table, insert_ouradaily, create_state_trigger_table, 
insert_state_triggers, read_oura_daily_data)
from H3_ingestionservice import fetch_oura, flatten_oura

def read_ouradata():
    conn = pgconnect()
    try:
        oura_data = read_oura_daily_data(conn)
    finally:
        conn.close()
    return oura_data

def upsrt_oura():
    fetched_data = fetch_oura()
    flattened_data = flatten_oura(fetched_data)

    conn = pgconnect()
    try:
        create_ouradaily_table(conn)
        insert_ouradaily(conn, flattened_data)
        conn.commit()
    finally:
        conn.close()
    print ("DB Write completed")

#below function needs to be rewritten for new table. 
def sendstatetriggersdb(statetriggers):
    conn = pgconnect()
    try:
        init_db(conn)
        create_state_trigger_table(conn)
        for trigger in statetriggers:
            insert_state_triggers(conn, trigger)
        conn.commit()
    finally:
        conn.close()

