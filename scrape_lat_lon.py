import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

INPUT_CSV = "data/airports_raw.csv"
OUTPUT_CSV = "data/airports_with_latlon.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; FlightScraper/1.0)"
}

df = pd.read_csv(INPUT_CSV)

latitudes = []
longitudes = []

for i, row in df.iterrows():
    airport_name = str(row["airport_name"])
    url = "https://en.wikipedia.org/wiki/" + airport_name.replace(" ", "_")

    print(f"⚡ Fast scraping: {airport_name}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            latitudes.append(None)
            longitudes.append(None)
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        lat_tag = soup.find("span", class_="latitude")
        lon_tag = soup.find("span", class_="longitude")

        latitudes.append(lat_tag.text if lat_tag else None)
        longitudes.append(lon_tag.text if lon_tag else None)

    except Exception:
        latitudes.append(None)
        longitudes.append(None)

    time.sleep(0.3)  # polite scraping

df["latitude"] = latitudes
df["longitude"] = longitudes

df.to_csv(OUTPUT_CSV, index=False)

print("✅ airports_with_latlon.csv created (FAST MODE)")
