import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load data
df = pd.read_csv(r"E:\Desktop\pome\model\data\processed\upi_processed.csv")

# Log transform
df["ln_value"] = np.log(df["upi_value_cr"])
df["ln_volume"] = np.log(df["upi_volume_cr"])
df["ln_gdp"] = np.log(df["national_gdp"])

# First differences (growth rates)
df["d_ln_value"] = df["ln_value"].diff()
df["d_ln_volume"] = df["ln_volume"].diff()
df["d_ln_gdp"] = df["ln_gdp"].diff()

df = df.dropna()

# Regression
X = sm.add_constant(df[["d_ln_volume", "d_ln_gdp"]])
y = df["d_ln_value"]

fd_model = sm.OLS(y, X).fit()
print(fd_model.summary())

# HAC standard errors

X = sm.add_constant(df[["ln_upi_volume", "ln_gdp"]])
y = df["ln_upi_value"]

hac_model = sm.OLS(y, X).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 3}
)

print(hac_model.summary())
