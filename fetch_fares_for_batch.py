import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# ================= CONFIG =================
BATCH_FILE = "data/route_batches/batch_001.csv"
OUTPUT_DIR = "data/fare_results"
PROGRESS_DIR = "data/progress"
SLEEP_SECONDS = 0.5   # API safety
# ==========================================

load_dotenv()

API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")

TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PROGRESS_DIR, exist_ok=True)

batch_name = os.path.basename(BATCH_FILE).replace(".csv", "")
OUTPUT_FILE = f"{OUTPUT_DIR}/{batch_name}_fares.csv"
PROGRESS_FILE = f"{PROGRESS_DIR}/{batch_name}_done.txt"


# ================= AUTH =================
def get_access_token():
    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": API_KEY,
            "client_secret": API_SECRET
        }
    )
    r.raise_for_status()
    return r.json()["access_token"]


# ================= LOAD PROGRESS =================
def load_processed_routes():
    if not os.path.exists(PROGRESS_FILE):
        return set()
    with open(PROGRESS_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())


def mark_done(route_key):
    with open(PROGRESS_FILE, "a") as f:
        f.write(route_key + "\n")


# ================= API CALL =================
def fetch_cheapest_fare(token, origin, destination):
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": "2025-01-15",
        "adults": 1,
        "currencyCode": "INR",
        "max": 1
    }

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(FLIGHT_URL, headers=headers, params=params)

    if r.status_code != 200:
        return None

    data = r.json().get("data", [])
    if not data:
        return None

    price = data[0]["price"]["grandTotal"]
    airline = data[0]["validatingAirlineCodes"][0]

    return airline, price


# ================= MAIN =================
def main():
    token = get_access_token()
    df = pd.read_csv(BATCH_FILE)

    processed = load_processed_routes()
    print(f"Already processed routes: {len(processed)}")

    # Create output file if not exists
    if not os.path.exists(OUTPUT_FILE):
        pd.DataFrame(columns=[
            "origin",
            "destination",
            "distance_km",
            "airline",
            "price_inr",
            "status"
        ]).to_csv(OUTPUT_FILE, index=False)

    for _, row in df.iterrows():
        route_key = f"{row.origin_iata}-{row.destination_iata}"

        if route_key in processed:
            continue

        try:
            result = fetch_cheapest_fare(
                token,
                row.origin_iata,
                row.destination_iata
            )

            if result:
                airline, price = result
                status = "FOUND"
            else:
                airline, price = None, None
                status = "NO_FLIGHT"

            output_row = pd.DataFrame([{
                "origin": row.origin_iata,
                "destination": row.destination_iata,
                "distance_km": row.distance_km,
                "airline": airline,
                "price_inr": price,
                "status": status
            }])

            output_row.to_csv(
                OUTPUT_FILE,
                mode="a",
                header=False,
                index=False
            )

            mark_done(route_key)
            print(f"✔ {route_key} → {status}")

            time.sleep(SLEEP_SECONDS)

        except Exception as e:
            print(f"❌ Error on {route_key}: {e}")
            time.sleep(2)
            continue


if __name__ == "__main__":
    main()
