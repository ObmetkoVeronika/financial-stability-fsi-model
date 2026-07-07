"""
Historical Financial Stability Index (FSI) calculation and visualization
for ATB-Market and MHP (2020-2023).
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Input data: financial indicators for both companies (example subset)
data = {
    "Year": [2020, 2021, 2022, 2023],
    "ATB_LIQ": [1.5, 1.7, 1.6, 1.8],
    "ATB_SOL": [0.4, 0.42, 0.41, 0.43],
    "ATB_PROF": [0.12, 0.14, 0.13, 0.15],
    "ATB_RISK": [0.1, 0.08, 0.09, 0.07],
    "MHP_LIQ": [1.2, 1.3, 1.35, 1.4],
    "MHP_SOL": [0.38, 0.4, 0.39, 0.41],
    "MHP_PROF": [0.1, 0.11, 0.12, 0.13],
    "MHP_RISK": [0.12, 0.1, 0.11, 0.09]
}

df = pd.DataFrame(data)

# Weighting coefficients
alpha_1 = 0.3  # Liquidity
alpha_2 = 0.3  # Solvency
alpha_3 = 0.25  # Profitability
alpha_4 = 0.15  # Risk

# Compute FSI for each company
df["ATB_FSI"] = (df["ATB_LIQ"] * alpha_1 +
                  df["ATB_SOL"] * alpha_2 +
                  df["ATB_PROF"] * alpha_3 -
                  df["ATB_RISK"] * alpha_4)
df["MHP_FSI"] = (df["MHP_LIQ"] * alpha_1 +
                  df["MHP_SOL"] * alpha_2 +
                  df["MHP_PROF"] * alpha_3 -
                  df["MHP_RISK"] * alpha_4)

# --- Visualization ---
plt.figure(figsize=(12, 6))
plt.plot(df["Year"], df["ATB_FSI"], label="ATB FSI", marker="o", color="blue")
plt.plot(df["Year"], df["MHP_FSI"], label="MHP FSI", marker="o", color="green")
plt.title("Financial Stability Index (FSI) Dynamics")
plt.xlabel("Year")
plt.ylabel("FSI")
plt.legend()
plt.grid(True)
plt.show()

# Individual component charts
coefficients = ["LIQ", "SOL", "PROF", "RISK"]
colors = ["purple", "orange", "red", "cyan"]

for i, coef in enumerate(coefficients):
    plt.figure(figsize=(10, 5))
    plt.plot(df["Year"], df[f"ATB_{coef}"], label=f"ATB {coef}", marker="o", color=colors[i])
    plt.plot(df["Year"], df[f"MHP_{coef}"], label=f"MHP {coef}", marker="o",
             linestyle="--", color=colors[i])
    plt.title(f"{coef} Dynamics — ATB vs MHP")
    plt.xlabel("Year")
    plt.ylabel(coef)
    plt.legend()
    plt.grid(True)
    plt.show()

# --- Summary statistics ---
print("Average Financial Stability Index:")
print(f"ATB: {df['ATB_FSI'].mean():.2f}")
print(f"MHP: {df['MHP_FSI'].mean():.2f}")

if df['ATB_FSI'].mean() > df['MHP_FSI'].mean():
    print("ATB shows higher average financial stability than MHP.")
else:
    print("MHP shows higher average financial stability than ATB.")

for coef in coefficients:
    atb_mean = df[f"ATB_{coef}"].mean()
    mhp_mean = df[f"MHP_{coef}"].mean()
    print(f"Average {coef}: ATB = {atb_mean:.2f}, MHP = {mhp_mean:.2f}")
    if atb_mean > mhp_mean:
        print(f"ATB has a higher average {coef} than MHP.")
    else:
        print(f"MHP has a higher average {coef} than ATB.")
