import pandas as pd
import random

# Load dataset
df = pd.read_csv("archive/keypoint.csv", header=None, on_bad_lines='skip')

# Copy dataframe
new_rows = []

# Existing labels probably 0–8
# Add extra fake labels 9–14

for i in range(9, 15):

    sample_rows = df.sample(100)

    sample_rows[0] = i

    new_rows.append(sample_rows)

# Merge
extended_df = pd.concat([df] + new_rows)

# Save
extended_df.to_csv("archive/extended_keypoint.csv", index=False, header=False)

print("Extended Dataset Created")
print("Shape:", extended_df.shape)