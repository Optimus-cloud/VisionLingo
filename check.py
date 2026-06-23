import pandas as pd
import os

for dataset in ["archive/keypoint.csv", "archive/extended_keypoint.csv"]:
    if os.path.exists(dataset):
        print(f"\n--- {dataset} ---")
        df = pd.read_csv(dataset, header=None)
        print("Shape:", df.shape)
        print("Unique Labels and Counts:")
        counts = df[0].value_counts().sort_index()
        for val, count in counts.items():
            print(f"  Class {val}: {count} samples")
    else:
        print(f"{dataset} does not exist.")