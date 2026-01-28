# Elasticity Based Decomposition of Digital Payment Methods

**A comprehensive analysis of UPI payment dynamics and their macroeconomic relationships**

This project presents a reproducible analysis pipeline that examines the elasticity of digital payment methods in India, specifically focusing on NPCI UPI (Unified Payments Interface) data alongside national and state GDP series (GSDP/MOSPI). The study investigates value–volume dynamics, decomposition patterns, and price elasticities to understand the behavioral economics underlying digital payment adoption and usage.

---

## Project Structure

Top-level folders (important files):

- `data/`
  - `raw/` — raw input files (UPI Excel files, MOSPI/GSDP raw files)
  - `processed/` — intermediate processed files (e.g., `national_gdp_annual1.csv`)
  - `final/` — final datasets for analysis (e.g., `upi_gdp_monthly.csv`, `upi_gdp_analysis.csv`)
- `scripts/` — ETL and cleaning scripts
  - `build_upi_panel.py` — detect & combine NPCI UPI Excel files into monthly national panel
  - `gsdp_cleaning.py` — cleans state GSDP raw data to tidy `state_gsdp_annual.csv`
  - `build_national_gdp.py` — aggregate state GSDP -> national GDP
  - `build_national_gdp_mospi.py` — fallback MOSPI-based routine (parses quarterly sheet to annual totals)
  - `merge_upi_gdp.py` — merge monthly UPI panel with annual GDP series
  - `finalize_analysis_data.py` — create final variables (logs, transformations) used in modelling
- `model/` — modelling & plotting code
  - `scripts/load.py` — basic preprocessing & save `upi_processed.csv`
  - `scripts/analysis.py` — plotting and elasticity regressions (Statsmodels)
  - `scripts/1delasticity.py` — first-difference elasticity models
- `results/` — figures and output visualizations (created by model code)
- `docs/` — documentation assets

---

## Quickstart (Recommended Run Order)

1. Create a Python virtual environment and install required packages (recommended):

```bash
python -m venv venv
# Windows
venv\Scripts\Activate.ps1  # or venv\Scripts\activate
pip install -r requirements.txt
```

2. Add your raw files into `data/raw/`:
- NPCI UPI Excel files named like `npci_upi_<year>.xlsx` (the `build_upi_panel.py` script looks for files starting with `npci_upi`)
- MOSPI quarterly file: `mospi_gdp_quarterly.xlsx` (used by `build_national_gdp_mospi.py`)
- GSDP raw (CSV or Excel) for `gsdp_cleaning.py`

3. Run the ETL scripts (from project root):

```bash
python scripts/build_upi_panel.py
python scripts/gsdp_cleaning.py
python scripts/build_national_gdp.py
python scripts/build_national_gdp_mospi.py   # optional fallback
python scripts/merge_upi_gdp.py
python scripts/finalize_analysis_data.py
```

4. Prepare model dataset & run analyses:

```bash
python model/scripts/load.py
python model/scripts/analysis.py
python model/scripts/1delasticity.py
```

5. Check generated files:
- `data/processed/` and `data/final/` for CSV datasets
- `model/results/` for plots and figures

---

## Expected Input/Output Files (Examples)

- Inputs (place in `data/raw/`)
  - `npci_upi_XXXX.xlsx` — NPCI UPI monthly files
  - `mospi_gdp_quarterly.xlsx` — MOSPI quarterly sheet
  - `gsdp_raw.csv` — state GSDP file (may require format adjustments)

- Processed / Final outputs
  - `data/processed/upi_monthly_all.csv`
  - `data/final/upi_panel_national_monthly.csv`
  - `data/processed/state_gsdp_annual.csv`
  - `data/processed/national_gdp_annual.csv`
  - `data/processed/national_gdp_annual1.csv`
  - `data/final/upi_gdp_monthly.csv`
  - `data/final/upi_gdp_analysis.csv`
  - `model/data/processed/upi_processed.csv`
  - `model/results/*.png`

---

## Important Notes & Assumptions

- Several scripts currently contain absolute Windows paths (e.g. `E:\Desktop\pome\...` in `scripts/gsdp_cleaning.py`, `model/scripts/*.py`). These should be changed to relative paths or parameterized for portability.
- `build_national_gdp_mospi.py` assumes MOSPI uses 2011 base and that quarterly values appear in repeating 4-column blocks; check the MOSPI file format before running.
- `build_upi_panel.py` expects column names containing keywords like `month`, `volume`, and `value` — slightly different column headers across NPCI releases may require small adjustments.
- Unit handling:
  - UPI volume in input appears to be in millions; script converts to `crore` by dividing by 10 and stores as `upi_volume_cr`.
  - GSDP values are expected in `Cr` (crore) or consistent units across states.

---

## Requirements

A minimal `requirements.txt` (also included in repo):

```
pandas
numpy
matplotlib
statsmodels
openpyxl
```

Note: pin versions if you need reproducible environments.

---

## Troubleshooting

- Missing input file error: ensure you placed the required files in `data/raw/` and/or update the script's `INPUT_FILE` path.
- `ValueError: Required columns not found` in `build_upi_panel.py`: open one of your NPCI files and inspect header names — update the column-detection logic or rename columns to match expected keywords.
- `Missing GDP values after merge` in `merge_upi_gdp.py`: verify `year` alignment (integer years) between UPI and GDP datasets.

---

## Recommended Improvements / TODOs

- Replace hard-coded absolute paths with a small CLI or config (e.g., `config.yaml`) and add argument parsing (`argparse`)
- Add a `requirements.txt` (done) and optionally environment locking with `pip-tools` or `conda` environment file
- Add unit tests for key cleaners (e.g., UPI header detection, MOSPI parsing)
- Create a small `Makefile` or `invoke` tasks to run the full pipeline reproducibly
- Add a license file and contributor guidelines

---

