import os
import pandas as pd

# ============================================================
# PATH SETUP (ROBUST)
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROC_DIR = os.path.join(BASE_DIR, "data", "processed")

INPUT_FILE = os.path.join(PROC_DIR, "state_gsdp_annual.csv")
OUTPUT_FILE = os.path.join(PROC_DIR, "national_gdp_annual.csv")

# ============================================================
# LOAD DATA
# ============================================================

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE)

print("[INFO] Loaded state GSDP data")
print(df.head())

# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

required_cols = {"state", "year", "gsdp_current"}
missing = required_cols - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# ============================================================
# CLEAN DATA
# ============================================================

# Ensure numeric GDP values
df["gsdp_current"] = pd.to_numeric(df["gsdp_current"], errors="coerce")

# Drop rows with missing GDP or year
df = df.dropna(subset=["year", "gsdp_current"])

# ============================================================
# AGGREGATE TO NATIONAL GDP
# ============================================================

national_gdp = (
    df.groupby("year", as_index=False)["gsdp_current"]
      .sum()
      .rename(columns={"gsdp_current": "national_gdp"})
)

# Sort by year
national_gdp = national_gdp.sort_values("year")

# ============================================================
# SAVE OUTPUT
# ============================================================

national_gdp.to_csv(OUTPUT_FILE, index=False)

print("\n[✓] National GDP annual file created successfully.")
print(f" → {OUTPUT_FILE}")
print("\nPreview:")
print(national_gdp.head())
