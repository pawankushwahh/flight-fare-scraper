import time
import csv
from datetime import datetime, timedelta

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.driver import get_driver

# ---------------- CONFIG ----------------
INPUT_CSV = "data/routes_for_fare_scraping_hub.csv"
OUTPUT_CSV = "data/fares_raw.csv"

AIRLINE = "IndiGo"
SOURCE = "goindigo.in"

# Fixed travel date: today + 14 days
TRAVEL_DATE = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")

# DRY RUN LIMIT (IMPORTANT)
MAX_ROUTES = 100        # 🔥 change to 50 / 100 later
DELAY_BETWEEN = 1    # seconds (anti-blocking)

# ---------------------------------------

def build_search_url(origin, destination, date):
    # IndiGo one-way search URL (structure-based, not form automation)
    return (
        "https://www.goindigo.in/booking/"
        f"?origin={origin}&destination={destination}"
        f"&date={date}&tripType=ONE_WAY&passengers=1"
    )

# Prepare output CSV (append-safe)
file_exists = False
try:
    with open(OUTPUT_CSV, "r"):
        file_exists = True
except FileNotFoundError:
    pass

out_file = open(OUTPUT_CSV, "a", newline="", encoding="utf-8")
writer = csv.writer(out_file)

if not file_exists:
    writer.writerow([
        "origin_iata",
        "destination_iata",
        "airline",
        "travel_date",
        "fare_inr",
        "source",
        "scraped_at"
    ])

# Load routes
routes_df = pd.read_csv(INPUT_CSV).head(MAX_ROUTES)

driver = get_driver(headless=True)
wait = WebDriverWait(driver, 25)

for idx, row in routes_df.iterrows():
    origin = row["origin_iata"]
    destination = row["destination_iata"]

    print(f"✈️ Scraping fare: {origin} → {destination}")

    url = build_search_url(origin, destination, TRAVEL_DATE)

    try:
        driver.get(url)

        # Wait for price element (selector may change — this is expected)
        price_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(),'₹')]")
            )
        )

        price_text = price_element.text
        fare = int(
            price_text.replace("₹", "").replace(",", "").strip()
        )

        print(f"✅ Fare found: ₹{fare}")

    except (TimeoutException, NoSuchElementException):
        print("⚠️ Fare not found (page layout / no flights)")
        fare = None

    # Save result (even if fare is None — important for analysis)
    writer.writerow([
        origin,
        destination,
        AIRLINE,
        TRAVEL_DATE,
        fare,
        SOURCE,
        datetime.now().isoformat()
    ])
    out_file.flush()

    # Anti-blocking delay
    time.sleep(DELAY_BETWEEN)

driver.quit()
out_file.close()

print("✅ Fare scraping run completed")
