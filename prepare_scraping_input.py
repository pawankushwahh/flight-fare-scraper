import pandas as pd
import random

INPUT_CSV = "data/routes_distance_filtered.csv"
OUTPUT_CSV = "data/routes_for_fare_scraping.csv"

# Load routes
df = pd.read_csv(INPUT_CSV)

print(f"📏 Total available routes: {len(df)}")

# -------------------------
# Distance buckets (km)
# -------------------------
short_routes = df[(df["distance_km"] >= 100) & (df["distance_km"] < 500)]
medium_routes = df[(df["distance_km"] >= 500) & (df["distance_km"] < 1500)]
long_routes = df[(df["distance_km"] >= 1500) & (df["distance_km"] <= 3000)]

print("Short routes:", len(short_routes))
print("Medium routes:", len(medium_routes))
print("Long routes:", len(long_routes))

# -------------------------
# Sampling strategy
# -------------------------
N_SHORT = 120
N_MEDIUM = 220
N_LONG = 120

sampled_short = short_routes.sample(
    n=min(N_SHORT, len(short_routes)), random_state=42
)
sampled_medium = medium_routes.sample(
    n=min(N_MEDIUM, len(medium_routes)), random_state=42
)
sampled_long = long_routes.sample(
    n=min(N_LONG, len(long_routes)), random_state=42
)

# Combine samples
sampled_df = pd.concat(
    [sampled_short, sampled_medium, sampled_long],
    ignore_index=True
)

# Shuffle to avoid pattern
sampled_df = sampled_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
sampled_df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Routes selected for fare scraping: {len(sampled_df)}")
print(f"💾 Saved to {OUTPUT_CSV}")
