import os
import pandas as pd
import numpy as np

# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINAL_DIR = os.path.join(BASE_DIR, "data", "final")

INPUT_FILE = os.path.join(FINAL_DIR, "upi_gdp_monthly.csv")
OUTPUT_FILE = os.path.join(FINAL_DIR, "upi_gdp_analysis.csv")

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

# ============================================================
# KEEP ONLY VALID GDP YEARS
# ============================================================

df = df[df["year"] <= 2024].copy()

# ============================================================
# LOG TRANSFORM VARIABLES
# ============================================================

df["ln_upi_volume"] = np.log(df["upi_volume_cr"])
df["ln_upi_value"] = np.log(df["upi_value_cr"])
df["ln_gdp"] = np.log(df["national_gdp"])

# ============================================================
# SORT & SAVE
# ============================================================

df = df.sort_values(["year", "month"])

df.to_csv(OUTPUT_FILE, index=False)

print("[✓] Final regression dataset created")
print(f" → {OUTPUT_FILE}")
print("\nPreview:")
print(df.head())
