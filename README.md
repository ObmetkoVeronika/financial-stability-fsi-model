# Financial Stability Index (FSI) — Crisis Resilience Modeling for Ukrainian Companies

An economic modeling project that builds a composite Financial Stability Index (FSI) to compare how two real Ukrainian companies from different sectors weathered the COVID-19 crisis, then forecasts their stability trajectory under optimistic, base, and pessimistic scenarios.

## Companies Analyzed

- **MHP (Myronivsky Khliboproduct)** — a major agricultural/poultry producer, export-oriented.
- **ATB-Market** — Ukraine's largest grocery retail chain, domestically focused.

The pairing lets the model contrast an export-driven sector against a domestic consumer-staples sector under the same macro shock.

## Methodology

### 1. Composite Index Construction

The FSI combines four weighted financial dimensions:

```
FSI = α1·LIQ + α2·SOL + α3·PROF − α4·RISK
```

| Component | Definition | Weight |
|---|---|---|
| `LIQ` (Liquidity) | Cash & equivalents ÷ Current liabilities | 0.30 |
| `SOL` (Solvency/Autonomy) | Financial independence ratio | 0.30 |
| `PROF` (Profitability) | Net profit margin | 0.25 |
| `RISK` | Long-term liabilities ÷ Total assets | 0.15 |

### 2. Historical Analysis (2019–2023)

Financial statements were pulled from public disclosure data (clarity-project.info) covering pre-crisis, crisis, and recovery periods.

### 3. Forecasting

Linear regression models were fit independently for each of the four components (per company) against year, then projected 5 years forward (2024–2028) under three scenarios:

- **Optimistic**: +10% adjustment over the linear trend
- **Base**: unadjusted linear trend
- **Pessimistic**: −10% adjustment over the linear trend

## Key Findings

| Metric | ATB | MHP |
|---|---|---|
| Mean FSI (2019–2023) | **0.497** | 0.340 |
| Liquidity trend | 1.4 → 1.8 (improving) | 0.07–0.09 (persistently weak) |
| Risk peak (2020) | 0.12 | **0.57** (severe COVID-year spike) |
| Risk by 2023 | 0.07 | 0.06 (recovered) |

**Takeaway:** ATB maintained materially stronger liquidity and lower risk exposure throughout the pandemic, translating into a consistently higher FSI. MHP suffered a severe risk spike in 2020 (likely tied to export/logistics disruption) but converged toward ATB's risk profile by 2023, even as its liquidity position remained structurally weaker.

## Repository Structure

```
├── report.pdf              # Full write-up: theory, methodology, data, results
├── src/
│   ├── fsi_calculation.py  # Historical FSI computation + visualization
│   └── fsi_forecast.py     # Linear regression forecasting + scenario analysis
```

## Tools

Python (pandas, numpy, matplotlib, scikit-learn)

## Data Sources

1. MHP — [clarity-project.info/edr/25412361/finances](https://clarity-project.info/edr/25412361/finances)
2. ATB-Market — [clarity-project.info/edr/30487219/finances](https://clarity-project.info/edr/30487219/finances)
