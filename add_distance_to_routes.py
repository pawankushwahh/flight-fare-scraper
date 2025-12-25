import pandas as pd
import math

AIRPORTS_CSV = "data/airports_cleaned.csv"
ROUTES_CSV = "data/routes_all_possible.csv"
OUTPUT_CSV = "data/routes_with_distance.csv"

# -------------------------
# Load data
# -------------------------
airports_df = pd.read_csv(AIRPORTS_CSV)
routes_df = pd.read_csv(ROUTES_CSV)

# Keep only airports with valid coordinates
airports_df = airports_df[
    airports_df["latitude_decimal"].notna() &
    airports_df["longitude_decimal"].notna() &
    airports_df["iata"].notna()
]

# Build lookup: IATA -> (lat, lon)
coord_map = {
    row["iata"]: (row["latitude_decimal"], row["longitude_decimal"])
    for _, row in airports_df.iterrows()
}

# -------------------------
# Haversine formula
# -------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2 +
        math.cos(phi1) * math.cos(phi2) *
        math.sin(dlambda / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

# -------------------------
# Compute distance
# -------------------------
distances = []

missing = 0

for _, row in routes_df.iterrows():
    src = row["origin_iata"]
    dst = row["destination_iata"]

    if src not in coord_map or dst not in coord_map:
        distances.append(None)
        missing += 1
        continue

    lat1, lon1 = coord_map[src]
    lat2, lon2 = coord_map[dst]

    dist = haversine(lat1, lon1, lat2, lon2)
    distances.append(dist)

routes_df["distance_km"] = distances

# -------------------------
# Save output
# -------------------------
routes_df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ routes_with_distance.csv created")
print(f"📏 Total routes: {len(routes_df)}")
print(f"⚠️ Routes with missing distance: {missing}")
