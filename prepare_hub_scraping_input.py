import pandas as pd

INPUT_CSV = "data/routes_distance_filtered.csv"
OUTPUT_CSV = "data/routes_for_fare_scraping_hub.csv"

# Major Indian airline hubs
HUBS = {
    "DEL", "BOM", "BLR", "HYD", "MAA", "CCU",
    "PNQ", "AMD", "COK", "TRV"
}

# Load distance-filtered routes
df = pd.read_csv(INPUT_CSV)

print(f"📏 Total distance-filtered routes: {len(df)}")

# Keep only hub-involved routes
hub_routes = df[
    (df["origin_iata"].isin(HUBS)) |
    (df["destination_iata"].isin(HUBS))
].copy()

print(f"✈️ Hub-involved routes available: {len(hub_routes)}")

# Sample routes for scraping (scraping-heavy but safe)
SAMPLE_SIZE = min(250, len(hub_routes))

sampled_routes = hub_routes.sample(
    n=SAMPLE_SIZE,
    random_state=42
)

# Save
sampled_routes.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Routes prepared for fare scraping: {len(sampled_routes)}")
print(f"💾 Saved to {OUTPUT_CSV}")
