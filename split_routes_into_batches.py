import os
import pandas as pd
import math

# ---------------- CONFIG ----------------
INPUT_CSV = "data/routes_distance_filtered.csv"
OUTPUT_DIR = "data/route_batches"
BATCH_SIZE = 500
# ----------------------------------------

def split_into_batches():
    # Create output directory if not exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load CSV
    df = pd.read_csv(INPUT_CSV)

    total_rows = len(df)
    total_batches = math.ceil(total_rows / BATCH_SIZE)

    print(f"Total routes       : {total_rows}")
    print(f"Batch size         : {BATCH_SIZE}")
    print(f"Total batches      : {total_batches}")

    for batch_num in range(total_batches):
        start = batch_num * BATCH_SIZE
        end = start + BATCH_SIZE

        batch_df = df.iloc[start:end]

        batch_filename = f"batch_{batch_num + 1:03d}.csv"
        batch_path = os.path.join(OUTPUT_DIR, batch_filename)

        batch_df.to_csv(batch_path, index=False)

        print(f"Saved {batch_filename} ({len(batch_df)} routes)")

    print("\n✅ All batches created successfully!")

if __name__ == "__main__":
    split_into_batches()
