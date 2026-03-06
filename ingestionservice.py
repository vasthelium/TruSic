# coding here for Ingestion service WO
import os
from urllib.parse import urlencode
import json
import httpx
#need import from postgres for tables and upsert here. 
from datetime import date, timedelta
from postgresdb import pgconnect, create_ouradaily_table, insert_ouradaily

#config
OURA_ACCESS_TOKEN = os.getenv("OURA_ACCESS_TOKEN", "")
def fetch_oura():
    if not OURA_ACCESS_TOKEN:
        raise ValueError("Oura access Token missing")
    
    Base_URL = "https://api.ouraring.com/v2/usercollection/sleep"
    today = date.today()
    yesterday = today - timedelta(days=1)
    params={"start_date": yesterday.isoformat(), "end_date": today.isoformat()}

    query = urlencode(params)
    cur_url = f"{Base_URL}?{query}"
    headers = {"Authorization":f"Bearer {OURA_ACCESS_TOKEN}"}

    with httpx.Client() as client:
        resp = client.get(cur_url, headers=headers)
        resp.raise_for_status()
    if resp.status_code!=200:
        raise ValueError("response not 200")
    raw_data = resp.json()
    return raw_data

def flatten_oura(raw_data: dict):
    oura_daily = []

    for data in raw_data.get("data", []):
        #some direct fields
        id = data["id"]
        average_heart_rate = data["average_heart_rate"]
        deep_sleep_duration = data["deep_sleep_duration"]
        light_sleep_duration = data["light_sleep_duration"]
        rem_sleep_duration = data["rem_sleep_duration"]
        total_sleep_duration = data["total_sleep_duration"]
        average_hrv = data["average_hrv"]
        #nested HRV
        hrv_interval = data.get("hrv", {}).get("interval")

        #nested readiness
        body_temperature = data.get("readiness", {}).get("contributors", {}).get("body_temperature")
        resting_heart_rate = data.get("readiness", {}).get("contributors", {}).get("resting_heart_rate")
        hrv_balance = data.get("readiness", {}).get("contributors", {}).get("hrv_balance")
        sleep_balance = data.get("readiness", {}).get("contributors", {}).get("sleep_balance")
        sleep_regularity = data.get("readiness", {}).get("contributors", {}).get("sleep_regularity")
        readiness_score = data.get("readiness", {}).get("score")

        flat_data = {
            "id": id,
            "average_heart_rate": average_heart_rate,
            "average_hrv": average_hrv,
            "hrv_interval": hrv_interval,
            "deep_sleep_duration": deep_sleep_duration,
            "light_sleep_duration": light_sleep_duration,
            "rem_sleep_duration": rem_sleep_duration,
            "total_sleep_duration": total_sleep_duration,
            "body_temperature": body_temperature,
            "resting_heart_rate": resting_heart_rate,
            "hrv_balance": hrv_balance,
            "sleep_balance": sleep_balance,
            "sleep_regularity": sleep_regularity,
            "readiness_score": readiness_score
            }
        oura_daily.append(flat_data)
    return oura_daily


def upsrt_oura():
    fetched_data = fetch_oura()
    flattened_data = flatten_oura(fetched_data)

    conn = pgconnect()
    create_ouradaily_table(conn)
    insert_ouradaily(conn, flattened_data)

    conn.close()
