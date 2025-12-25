import os
import pandas as pd
from utils.driver import get_driver

URL = "https://en.wikipedia.org/wiki/List_of_airports_in_India"

os.makedirs("data/raw_html", exist_ok=True)

driver = get_driver(headless=True)
driver.get(URL)

html = driver.page_source

# Save raw HTML (always do this)
with open("data/raw_html/airports.html", "w", encoding="utf-8") as f:
    f.write(html)

driver.quit()

# 🔥 KEY LINE — extract ALL tables
tables = pd.read_html(html)

records = []

for table in tables:
    cols = [c.lower() for c in table.columns.astype(str)]

    # Identify airport tables
    if "iata" in cols and "icao" in cols:
        for _, row in table.iterrows():
            records.append({
                "airport_name": row.iloc[0],
                "city": row.iloc[1],
                "iata": row.iloc[2],
                "icao": row.iloc[3],
                "type": row.iloc[4],
                "source": "Wikipedia"
            })

df = pd.DataFrame(records)
df.to_csv("data/airports_raw.csv", index=False)

print(f"✅ airports_raw.csv created with {len(df)} rows")
