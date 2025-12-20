import os
import pandas as pd

# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FINAL_DIR = os.path.join(BASE_DIR, "data", "final")
PROC_DIR = os.path.join(BASE_DIR, "data", "processed")

UPI_FILE = os.path.join(FINAL_DIR, "upi_panel_national_monthly.csv")
GDP_FILE = os.path.join(PROC_DIR, "national_gdp_annual1.csv")

OUTPUT_FILE = os.path.join(FINAL_DIR, "upi_gdp_monthly.csv")

# ============================================================
# LOAD DATA
# ============================================================

upi = pd.read_csv(UPI_FILE)
gdp = pd.read_csv(GDP_FILE)

print("[INFO] Loaded UPI and GDP data")

# ============================================================
# MERGE (ANNUAL GDP → MONTHLY UPI)
# ============================================================

df = upi.merge(gdp, on="year", how="left")

# ============================================================
# VALIDATION
# ============================================================

if df["national_gdp"].isna().any():
    raise ValueError("Missing GDP values after merge — check year alignment")

# ============================================================
# SAVE FINAL DATASET
# ============================================================

df.to_csv(OUTPUT_FILE, index=False)

print("\n[✓] Final modeling dataset created")
print(f" → {OUTPUT_FILE}")
print("\nPreview:")
print(df.head())
