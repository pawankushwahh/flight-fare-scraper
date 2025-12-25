import pandas as pd
import re

INPUT_CSV = "data/airports_with_latlon.csv"
OUTPUT_CSV = "data/airports_cleaned.csv"

df = pd.read_csv(INPUT_CSV)

def dms_to_decimal(dms):
    if pd.isna(dms):
        return None

    # Pattern with seconds
    pattern_full = r"(\d+)°(\d+)′(\d+)″([NSEW])"
    # Pattern without seconds
    pattern_partial = r"(\d+)°(\d+)′([NSEW])"

    match = re.match(pattern_full, dms)
    if match:
        degrees, minutes, seconds, direction = match.groups()
        decimal = (
            float(degrees)
            + float(minutes) / 60
            + float(seconds) / 3600
        )
    else:
        match = re.match(pattern_partial, dms)
        if not match:
            return None
        degrees, minutes, direction = match.groups()
        decimal = float(degrees) + float(minutes) / 60

    if direction in ["S", "W"]:
        decimal *= -1

    return round(decimal, 6)

df["latitude_decimal"] = df["latitude"].apply(dms_to_decimal)
df["longitude_decimal"] = df["longitude"].apply(dms_to_decimal)

df.to_csv(OUTPUT_CSV, index=False)

print("✅ airports_cleaned.csv created")
