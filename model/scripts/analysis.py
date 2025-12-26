# ================================
# UPI Value–Volume Divergence Analysis
# ================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# ----------------
# STEP 3: Load data
# ----------------
df = pd.read_csv(r"E:\Desktop\pome\model\data\processed\upi_processed.csv")  # change filename if needed

# Ensure correct ordering
df = df.sort_values(["year", "month"]).reset_index(drop=True)

# -----------------------------
# STEP 4: Data integrity fix
# Drop incomplete 2025-12 entry
# -----------------------------
df = df[~((df["year"] == 2025) & (df["month"] == 12))].reset_index(drop=True)

# -----------------------------
# STEP 5: Feature engineering
# -----------------------------
df["ln_upi_value"] = np.log(df["upi_value_cr"])
df["ln_upi_volume"] = np.log(df["upi_volume_cr"])
df["ln_gdp"] = np.log(df["national_gdp"])

# Growth rates (monthly log differences)
df["g_upi_value"] = df["ln_upi_value"].diff()
df["g_upi_volume"] = df["ln_upi_volume"].diff()

# Average ticket size
df["avg_ticket"] = df["upi_value_cr"] / df["upi_volume_cr"]
df["ln_avg_ticket"] = np.log(df["avg_ticket"])

# Remove first row after diff
df = df.dropna().reset_index(drop=True)

# -----------------------------
# STEP 6: Divergence metric
# -----------------------------
df["divergence"] = df["g_upi_value"] - df["g_upi_volume"]

# -----------------------------
# Sanity checks
# -----------------------------
print("\n=== Summary Statistics ===")
print(df[["avg_ticket", "g_upi_value", "g_upi_volume", "divergence"]].describe())

# -----------------------------
# Visualization 1:
# Growth comparison
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(df["ym"], df["g_upi_value"], label="Value Growth", marker="o")
plt.plot(df["ym"], df["g_upi_volume"], label="Volume Growth", marker="o")
plt.xticks(rotation=90)
plt.title("UPI Value vs Volume Growth")
plt.legend()
plt.tight_layout()
plt.savefig(r"E:\Desktop\pome\model\results\upi_value_volume_growth.png")
plt.show()

# -----------------------------
# Visualization 2:
# Divergence over time
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(df["ym"], df["divergence"], color="black", marker="o")
plt.axhline(0, linestyle="--")
plt.xticks(rotation=90)
plt.title("Value–Volume Divergence")
plt.tight_layout()
plt.savefig(r"E:\Desktop\pome\model\results\value_volume_divergence.png")
plt.show()

# -----------------------------
# Elasticity Model 1:
# ln(Value) ~ ln(Volume) + ln(GDP)
# -----------------------------
X1 = sm.add_constant(df[["ln_upi_volume", "ln_gdp"]])
y1 = df["ln_upi_value"]

model_value = sm.OLS(y1, X1).fit()

# -----------------------------
# Elasticity Model 2:
# ln(Volume) ~ ln(GDP)
# -----------------------------
X2 = sm.add_constant(df[["ln_gdp"]])
y2 = df["ln_upi_volume"]

model_volume = sm.OLS(y2, X2).fit()

# -----------------------------
# Results
# -----------------------------
print("\n=== Elasticity Results ===")
print("\nValue Elasticity Model:")
print(model_value.summary())

print("\nVolume Elasticity Model:")
print(model_volume.summary())

# -----------------------------
# Interpretation helper
# -----------------------------
beta_value = model_value.params["ln_upi_volume"]
beta_volume = model_volume.params["ln_gdp"]

print("\n=== Key Elasticities ===")
print(f"Value–Volume Elasticity (β_v): {beta_value:.3f}")
print(f"Volume–GDP Elasticity (β_q): {beta_volume:.3f}")
