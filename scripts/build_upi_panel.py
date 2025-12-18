import os
import glob
import pandas as pd

# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = "."
RAW_DIR = f"{BASE_DIR}/data/raw"
PROC_DIR = f"{BASE_DIR}/data/processed"
FINAL_DIR = f"{BASE_DIR}/data/final"

os.makedirs(PROC_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

print("[OK] Folder structure ready.")

# ============================================================
# RAW FILE DETECTION
# ============================================================

FOUND = {"npci_upi": None}

for f in os.listdir(RAW_DIR):
    if f.lower().endswith(".xlsx") and "upi" in f.lower():
        FOUND["npci_upi"] = f"{RAW_DIR}/{f}"
        break

print("\n=== RAW FILE CHECK ===")
if FOUND["npci_upi"]:
    print(f"[FOUND]   npci_upi → {FOUND['npci_upi']}")
else:
    print("[MISSING] npci_upi")
    exit()

# ============================================================
# CLEAN NPCI UPI DATA (UNIT-SAFE)
# ============================================================

def clean_upi(filepath):
    print("[*] Cleaning NPCI UPI data...")

    df = pd.read_excel(filepath)

    # Normalize column names
    df.columns = (
        df.columns.str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace(".", "", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
    )

    print("[INFO] Columns detected:")
    for c in df.columns:
        print("  ", c)

    # Identify columns
    month_col = None
    volume_mn_col = None
    value_cr_col = None

    for c in df.columns:
        if "month" in c:
            month_col = c
        if "volume" in c and "mn" in c and "avg" not in c:
            volume_mn_col = c
        if "value" in c and "cr" in c and "avg" not in c:
            value_cr_col = c

    if not all([month_col, volume_mn_col, value_cr_col]):
        raise ValueError("Required columns not found. Check column names above.")

    # Create clean dataframe
    df = df[[month_col, volume_mn_col, value_cr_col]].copy()
    df.columns = ["ym", "upi_volume_mn", "upi_value_cr"]

    # Convert Volume Mn → Cr
    df["upi_volume_cr"] = df["upi_volume_mn"] / 10

    # Parse month
    df["ym"] = pd.to_datetime(df["ym"], errors="coerce")
    df = df.dropna(subset=["ym"])

    df["year"] = df["ym"].dt.year
    df["month"] = df["ym"].dt.month
    df["ym"] = df["ym"].dt.strftime("%Y-%m")

    # Keep only standardized columns
    df = df[["ym", "year", "month", "upi_volume_cr", "upi_value_cr"]]

    outpath = f"{PROC_DIR}/upi_monthly.csv"
    df.to_csv(outpath, index=False)

    print("[✓] UPI cleaned successfully.")
    print(f"[✓] Saved → {outpath}")

    return df

# ============================================================
# RUN CLEANING
# ============================================================

clean_upi(FOUND["npci_upi"])

# ============================================================
# FINAL PANEL (UPI ONLY FOR NOW)
# ============================================================

panel = pd.read_csv(f"{PROC_DIR}/upi_monthly.csv")
panel.to_csv(f"{FINAL_DIR}/upi_panel_state_monthly.csv", index=False)

print("\n[✓] Final panel saved:")
print(f"{FINAL_DIR}/upi_panel_state_monthly.csv")
