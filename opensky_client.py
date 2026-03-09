import requests
from datetime import datetime, timedelta
import time
import warnings
import os
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
 # load .env from current directory
load_dotenv()

TOKEN_URL = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
STATES_URL = "https://opensky-network.org/api/states/all"

# read from .env
CLIENT_ID = os.getenv("OPENSKY_CLIENT_ID")
CLIENT_SECRET = os.getenv("OPENSKY_CLIENT_SECRET")

access_token = None
token_expiry = datetime.utcnow()

def refresh_token():
    global access_token, token_expiry

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    print("Refreshing token...")
    print("CLIENT_ID:", CLIENT_ID)
    print("CLIENT_SECRET is None?", CLIENT_SECRET is None)

    resp = requests.post(TOKEN_URL, data=data)
    print("Token status code:", resp.status_code)
    print("Token response text:", resp.text)
    resp.raise_for_status()

    response_json = resp.json()
    access_token = response_json["access_token"]
    expires_in = response_json["expires_in"]
    token_expiry = datetime.utcnow() + timedelta(seconds=expires_in - 60)
    print("New token acquired, expires in (sec):", expires_in)

def get_states():
    global access_token, token_expiry

    if access_token is None or datetime.utcnow() >= token_expiry:
        refresh_token()

    headers = {"Authorization": f"Bearer {access_token}"}
    
    
    resp = requests.get(STATES_URL, headers=headers)

    if resp.status_code == 401:
        print("Got 401 on states, refreshing token and retrying...")
        refresh_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        resp = requests.get(STATES_URL, headers=headers)

    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 15))
        print(f"Rate limited (429). Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        resp = requests.get(STATES_URL, headers=headers)

    if resp.status_code == 429:
        print("Still rate limited after retry. Skipping this round.")
        return {"states": [], "time": 0}

    resp.raise_for_status()

    return resp.json()

if __name__ == "__main__":
    while True:
        data = get_states()
        states = data.get("states", [])
        print("Snapshot:", data["time"], "count:", len(states))

        flights = []
        for s in states[::]:
            flights.append({
                "icao24": s[0],
                "callsign": s[1],
                "origin_country": s[2],
                "time_position": s[3],
                "last_contact": s[4],
                "longitude": s[5],
                "latitude": s[6],
                "geo_altitude": s[13],
                "on_ground": s[8],
                "velocity": s[9],
                "heading": s[10],
                "vertical_rate": s[11],
            })

        print("Sample flights:", flights)
        time.sleep(30)
