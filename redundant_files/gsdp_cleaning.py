import pandas as pd
import re
import os

# -----------------------------
# Paths
# -----------------------------
INPUT_FILE = r"E:\Desktop\pome\data\raw\mospi\gsdp_raw.csv"   # change to .xlsx if needed
OUTPUT_FILE = "data/processed/state_gsdp_annual.csv"

os.makedirs("data/processed", exist_ok=True)

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(INPUT_FILE)

# Standardize column names
df.columns = df.columns.str.strip()

# Rename state column
df.rename(columns={"State/Uts": "state"}, inplace=True)

# -----------------------------
# Keep only GSDP current price columns
# -----------------------------
gsdp_cols = [
    c for c in df.columns
    if c.startswith("GSDP-Curr")
]

df_gsdp = df[["state"] + gsdp_cols]

# -----------------------------
# Convert wide → long
# -----------------------------
df_long = df_gsdp.melt(
    id_vars="state",
    value_vars=gsdp_cols,
    var_name="year_range",
    value_name="gsdp_current"
)

# -----------------------------
# Extract year from column name
# Example: GSDP-Curr-2016-17(Cr) → 2016
# -----------------------------
df_long["year"] = df_long["year_range"].apply(
    lambda x: int(re.search(r"(\d{4})-\d{2}", x).group(1))
)

# -----------------------------
# Clean values
# -----------------------------
df_long["gsdp_current"] = (
    df_long["gsdp_current"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .replace("NA", pd.NA)
    .astype(float)
)

# -----------------------------
# Final tidy dataset
# -----------------------------
df_final = (
    df_long[["state", "year", "gsdp_current"]]
    .sort_values(["state", "year"])
    .reset_index(drop=True)
)

# -----------------------------
# Save
# -----------------------------
df_final.to_csv(OUTPUT_FILE, index=False)

print("✅ Clean GSDP dataset created:")
print(OUTPUT_FILE)
print(df_final.head())
