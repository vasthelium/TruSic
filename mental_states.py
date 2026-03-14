##imports here. 
from postgresdb import pgconnect, read_oura_daily_data

def healthstat():
    conn = pgconnect()
    oura_data = read_oura_daily_data(conn)
    conn.close()

    #Derive the needed OURA data
    day = oura_data["day"]
    sleep_score = oura_data["sleep_score"]
    total_sleep_duration = oura_data["total_sleep_duration"]/3600
    average_hrv = oura_data["average_hrv"]
    resting_heart_rate = oura_data["resting_heart_rate"]
    readiness_score = oura_data["readiness_score"]

    #mock Steps #baselined 9000
    steps = 9000
    baseline_hrv = 60
    hrv_balance = average_hrv / baseline_hrv
    cognitive_state = (sleep_score * hrv_balance) / steps

    return cognitive_state



#     #---DB wiring for daily data read of two values---
#     conn = pgconnect()
#     oura = read_oura_daily(conn)
#     google = read_google_daily(conn)
#     conn.close()

#     #deriving the total sleep & steps
#     sleep_hrs = round((oura["total_sleep"] / 100) * 9, 2)
#     calibration_offset = 4500
#     prev_day_steps = google["steps"] + calibration_offset

#     print(sleep_hrs, "is your sleep hrs")
#     print(prev_day_steps, "your previous day steps")

#     Health_ip = {
#        "sleep_hrs" : sleep_hrs,
#        "resting_hrv" : 60, #fixed baseline
#        "prev_day_steps" : prev_day_steps,
#     }
#     return Health_ip

