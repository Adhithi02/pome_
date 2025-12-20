import os
import pandas as pd
import numpy as np

# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROC_DIR = os.path.join(BASE_DIR, "data", "processed")

INPUT_FILE = os.path.join(RAW_DIR, "mospi_gdp_quarterly.xlsx")
OUTPUT_FILE = os.path.join(PROC_DIR, "national_gdp_annual1.csv")

# ============================================================
# LOAD FULL SHEET (NO HEADERS)
# ============================================================

df = pd.read_excel(INPUT_FILE, header=None)

print("[INFO] MOSPI sheet loaded")

# ============================================================
# FIND LAST NUMERIC ROW (TOTAL GDP)
# ============================================================

numeric_rows = df.apply(
    lambda row: pd.to_numeric(row, errors="coerce").notna().sum(),
    axis=1
)

# Row with maximum numeric entries = GDP total row
gdp_row_idx = numeric_rows.idxmax()

print(f"[INFO] GDP row detected at Excel row {gdp_row_idx}")

gdp_row = pd.to_numeric(df.loc[gdp_row_idx], errors="coerce")

# ============================================================
# EXTRACT QUARTERS BY POSITION
# ============================================================
# MOSPI structure:
# Every 4 columns = Q1 Q2 Q3 Q4 for one year
# Data starts after first 1–2 descriptor columns
# ============================================================

values = gdp_row.dropna().values

# Remove first column if it's an index/serial
if len(values) % 4 != 0:
    values = values[1:]

years = []
gdp_vals = []

start_year = 2011  # MOSPI 2011–12 base

for i in range(0, len(values), 4):
    year = start_year + (i // 4)
    annual_gdp = values[i:i+4].sum()

    years.append(year)
    gdp_vals.append(annual_gdp)

# ============================================================
# BUILD FINAL DATAFRAME
# ============================================================

gdp_annual = pd.DataFrame({
    "year": years,
    "national_gdp": gdp_vals
})

gdp_annual = gdp_annual.sort_values("year")

# ============================================================
# SAVE OUTPUT
# ============================================================

gdp_annual.to_csv(OUTPUT_FILE, index=False)

print("\n[✓] National GDP (annual, current prices) created")
print(f" → {OUTPUT_FILE}")
print("\nPreview:")
print(gdp_annual.head())
