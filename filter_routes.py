import pandas as pd

INPUT_CSV = "data/routes_with_distance.csv"

DISTANCE_FILTERED_CSV = "data/routes_distance_filtered.csv"
HUB_FILTERED_CSV = "data/routes_likely.csv"

# Define hub airports
HUBS = {"DEL", "BOM", "BLR", "HYD", "MAA", "CCU"}

# Load routes
df = pd.read_csv(INPUT_CSV)

print(f"📏 Total routes before filtering: {len(df)}")

# -------------------------
# Rule 1: Distance filter
# -------------------------
distance_filtered = df[
    (df["distance_km"] >= 100) &
    (df["distance_km"] <= 3000)
].copy()

distance_filtered.to_csv(DISTANCE_FILTERED_CSV, index=False)

print(f"✂️ After distance filter: {len(distance_filtered)}")
print(f"💾 Saved to {DISTANCE_FILTERED_CSV}")

# -------------------------
# Rule 2: Hub filter
# -------------------------
hub_filtered = distance_filtered[
    (distance_filtered["origin_iata"].isin(HUBS)) |
    (distance_filtered["destination_iata"].isin(HUBS))
].copy()

hub_filtered.to_csv(HUB_FILTERED_CSV, index=False)

print(f"✂️ After hub filter: {len(hub_filtered)}")
print(f"💾 Saved to {HUB_FILTERED_CSV}")
