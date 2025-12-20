import os
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
# DETECT ALL NPCI UPI FILES
# ============================================================

upi_files = []

for f in os.listdir(RAW_DIR):
    if f.lower().endswith(".xlsx") and f.lower().startswith("npci_upi"):
        upi_files.append(os.path.join(RAW_DIR, f))

if not upi_files:
    print("[ERROR] No NPCI UPI files found in data/raw/")
    exit()

print("\n[FOUND] NPCI UPI files:")
for f in sorted(upi_files):
    print("  ", f)

# ============================================================
# CLEAN FUNCTION (REUSED FOR EACH YEAR)
# ============================================================

def clean_upi(filepath):
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

    # Identify required columns
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
        raise ValueError(f"Required columns not found in {filepath}")

    df = df[[month_col, volume_mn_col, value_cr_col]].copy()
    df.columns = ["ym", "upi_volume_mn", "upi_value_cr"]

    # Unit conversion
    df["upi_volume_cr"] = df["upi_volume_mn"] / 10

    # Parse month
    df["ym"] = pd.to_datetime(df["ym"], errors="coerce")
    df = df.dropna(subset=["ym"])

    df["year"] = df["ym"].dt.year
    df["month"] = df["ym"].dt.month
    df["ym"] = df["ym"].dt.strftime("%Y-%m")

    return df[["ym", "year", "month", "upi_volume_cr", "upi_value_cr"]]

# ============================================================
# CLEAN & STACK ALL YEARS
# ============================================================

all_dfs = []

for file in sorted(upi_files):
    print(f"[*] Processing {file}")
    df_clean = clean_upi(file)
    all_dfs.append(df_clean)

final_upi = pd.concat(all_dfs, ignore_index=True)

# Remove duplicates and sort
final_upi = final_upi.drop_duplicates(subset=["ym"])
final_upi = final_upi.sort_values("ym")

# ============================================================
# SAVE OUTPUTS
# ============================================================

final_upi.to_csv(f"{PROC_DIR}/upi_monthly_all.csv", index=False)
final_upi.to_csv(f"{FINAL_DIR}/upi_panel_national_monthly.csv", index=False)

print("\n[✓] Combined national UPI dataset created.")
print(f" → {PROC_DIR}/upi_monthly_all.csv")
print(f" → {FINAL_DIR}/upi_panel_national_monthly.csv")
