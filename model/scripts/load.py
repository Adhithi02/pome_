import pandas as pd
import numpy as np

# Load data
df = pd.read_csv(r"E:\Desktop\pome\model\data\raw\upi_gdp_monthly.csv")

# Sort chronologically
df = df.sort_values(["year", "month"]).reset_index(drop=True)

# Check for missing values
print(df.isna().sum())

# Basic info
print(df.head())
print(df.tail())

# Log transformations
df["ln_upi_value"] = np.log(df["upi_value_cr"])
df["ln_upi_volume"] = np.log(df["upi_volume_cr"])
df["ln_gdp"] = np.log(df["national_gdp"])

# Growth rates (log differences)
df["g_upi_value"] = df["ln_upi_value"].diff()
df["g_upi_volume"] = df["ln_upi_volume"].diff()

# Average transaction value
df["avg_ticket"] = df["upi_value_cr"] / df["upi_volume_cr"]
df["ln_avg_ticket"] = np.log(df["avg_ticket"])

# Drop first row (diff produces NA)
df = df.dropna().reset_index(drop=True)

# Save processed data
df.to_csv(r"E:\Desktop\pome\model\data\processed\upi_processed.csv", index=False)

