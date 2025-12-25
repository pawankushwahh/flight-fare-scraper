import pandas as pd
import json

INPUT_CSV = "data/airports_cleaned.csv"
GRAPH_JSON = "data/routes_graph.json"
ROUTES_CSV = "data/routes_all_possible.csv"

# Load cleaned airport data
# df = pd.read_csv(INPUT_CSV)

# # Keep only valid IATA codes
# df = df[df["iata"].notna()]
# df["iata"] = df["iata"].str.strip()

# airports = df["iata"].unique().tolist()


# Load cleaned airport data
df = pd.read_csv("data/airports_cleaned.csv")

# KEEP ONLY airports with IATA + lat/lon
df = df[
    df["iata"].notna() &
    df["latitude_decimal"].notna() &
    df["longitude_decimal"].notna()
]

df["iata"] = df["iata"].str.strip().str.upper()

airports = df["iata"].unique().tolist()



print(f"✈️ Total airports: {len(airports)}")

# -------------------------
# Build adjacency list
# -------------------------
routes_graph = {}

for origin in airports:
    routes_graph[origin] = [dest for dest in airports if dest != origin]

# -------------------------
# Save graph as JSON
# -------------------------
with open(GRAPH_JSON, "w") as f:
    json.dump(routes_graph, f, indent=2)

# -------------------------
# Build flat route table
# -------------------------
rows = []

for origin, destinations in routes_graph.items():
    for dest in destinations:
        rows.append({
            "origin_iata": origin,
            "destination_iata": dest
        })

routes_df = pd.DataFrame(rows)
routes_df.to_csv(ROUTES_CSV, index=False)

print(f"✅ Graph saved to {GRAPH_JSON}")
print(f"✅ Routes table saved to {ROUTES_CSV}")
print(f"🔢 Total routes: {len(routes_df)}")
