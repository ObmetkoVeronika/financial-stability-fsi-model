"""
Financial Stability Index (FSI) forecasting for ATB-Market and MHP (2024-2028)
using linear regression, with optimistic/base/pessimistic scenario analysis.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Input data: financial indicators for both companies (2019-2023)
data = {
    "Year": [2019, 2020, 2021, 2022, 2023],
    "ATB_LIQ": [1.4, 1.5, 1.7, 1.6, 1.8],
    "ATB_SOL": [0.39, 0.4, 0.42, 0.41, 0.43],
    "ATB_PROF": [0.11, 0.12, 0.14, 0.13, 0.15],
    "ATB_RISK": [0.12, 0.1, 0.08, 0.09, 0.07],
    "MHP_LIQ": [0.07, 0.09, 0.04, 0.04, 0.07],
    "MHP_SOL": [0.37, 0.38, 0.4, 0.39, 0.41],
    "MHP_PROF": [0.09, 0.1, 0.11, 0.12, 0.13],
    "MHP_RISK": [0.34, 0.57, 0.27, 0.16, 0.06]
}

df = pd.DataFrame(data)

# Weighting coefficients
alpha_1 = 0.3
alpha_2 = 0.3
alpha_3 = 0.25
alpha_4 = 0.15


def linear_regression_model(x, y):
    model = LinearRegression()
    model.fit(x, y)
    return model


# Fit a separate linear model per indicator, per company
X = df["Year"].values.reshape(-1, 1)

models_atb = {
    "LIQ": linear_regression_model(X, df["ATB_LIQ"]),
    "SOL": linear_regression_model(X, df["ATB_SOL"]),
    "PROF": linear_regression_model(X, df["ATB_PROF"]),
    "RISK": linear_regression_model(X, df["ATB_RISK"])
}

models_mhp = {
    "LIQ": linear_regression_model(X, df["MHP_LIQ"]),
    "SOL": linear_regression_model(X, df["MHP_SOL"]),
    "PROF": linear_regression_model(X, df["MHP_PROF"]),
    "RISK": linear_regression_model(X, df["MHP_RISK"])
}

# Forecast horizon
future_years = np.array([2024, 2025, 2026, 2027, 2028]).reshape(-1, 1)

predictions_atb = {key: model.predict(future_years) for key, model in models_atb.items()}
predictions_mhp = {key: model.predict(future_years) for key, model in models_mhp.items()}


def scenario_predictions(predictions, scenario):
    """
    Apply a scenario adjustment to baseline linear predictions.
    Optimistic: +10%, Pessimistic: -10%, Base: unchanged.
    """
    if scenario == "optimistic":
        return {key: value * 1.1 for key, value in predictions.items()}
    elif scenario == "pessimistic":
        return {key: value * 0.9 for key, value in predictions.items()}
    else:
        return predictions


scenarios = ["optimistic", "base", "pessimistic"]
scenario_predictions_atb = {s: scenario_predictions(predictions_atb, s) for s in scenarios}
scenario_predictions_mhp = {s: scenario_predictions(predictions_mhp, s) for s in scenarios}


def calculate_fsi_predictions(pred_atb, pred_mhp):
    fsi_atb = (pred_atb["LIQ"] * alpha_1 +
               pred_atb["SOL"] * alpha_2 +
               pred_atb["PROF"] * alpha_3 -
               pred_atb["RISK"] * alpha_4)
    fsi_mhp = (pred_mhp["LIQ"] * alpha_1 +
               pred_mhp["SOL"] * alpha_2 +
               pred_mhp["PROF"] * alpha_3 -
               pred_mhp["RISK"] * alpha_4)
    return fsi_atb, fsi_mhp


fsi_atb_scenario = {
    s: calculate_fsi_predictions(scenario_predictions_atb[s], scenario_predictions_mhp[s])[0]
    for s in scenarios
}
fsi_mhp_scenario = {
    s: calculate_fsi_predictions(scenario_predictions_atb[s], scenario_predictions_mhp[s])[1]
    for s in scenarios
}

# --- Visualization ---
plt.figure(figsize=(12, 6))
for scenario in scenarios:
    plt.plot(future_years, fsi_atb_scenario[scenario], label=f"ATB FSI ({scenario})", marker="o")
    plt.plot(future_years, fsi_mhp_scenario[scenario], label=f"MHP FSI ({scenario})",
              marker="x", linestyle="--")

plt.title("FSI Forecast by Scenario — ATB vs MHP (2024-2028)")
plt.xlabel("Year")
plt.ylabel("FSI")
plt.legend()
plt.grid(True)
plt.show()

# --- Printed results ---
for scenario in scenarios:
    print(f"\n{scenario.capitalize()} scenario forecast:")
    for year, atb_fsi, mhp_fsi in zip(future_years.flatten(),
                                        fsi_atb_scenario[scenario],
                                        fsi_mhp_scenario[scenario]):
        print(f"{year}: ATB FSI = {atb_fsi:.2f}, MHP FSI = {mhp_fsi:.2f}")
