from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


required_files = [
    "data/male_mortality_2000_2016.xlsx",
    "data/female_mortality_2000_2016.xlsx",
    "stan/lc.stan",
    "stan/apc.stan",
    "stan/cbd_lr.stan",
    "stan/rh.stan",
    "results/full_period/combined_four_model_comparison.csv",
    "results/chronological/four_model_chronological_validation.csv",
    "results/forecasts/life_expectancy_forecasts_to_2040.csv",
    "results/forecasts/rh_age_specific_mortality_forecasts_to_2040.csv",
    "results/validation/mcmc_diagnostics.csv",
    "results/validation/srs_life_expectancy_validation.csv",
]

missing = [name for name in required_files if not (ROOT / name).exists()]
if missing:
    raise FileNotFoundError(f"Missing required repository files: {missing}")

full = pd.read_csv(ROOT / "results/full_period/combined_four_model_comparison.csv")
chron = pd.read_csv(ROOT / "results/chronological/four_model_chronological_validation.csv")
diag = pd.read_csv(ROOT / "results/validation/mcmc_diagnostics.csv")
srs = pd.read_csv(ROOT / "results/validation/srs_life_expectancy_validation.csv")
e0 = pd.read_csv(ROOT / "results/forecasts/life_expectancy_forecasts_to_2040.csv")
rates = pd.read_csv(ROOT / "results/forecasts/rh_age_specific_mortality_forecasts_to_2040.csv")

assert set(full["model"]) == {"LC", "APC", "CBD-LR", "RH"}
assert full.sort_values("elpd_loo", ascending=False).iloc[0]["model"] == "RH"
assert abs(float(full.loc[full.model == "RH", "elpd_loo"].iloc[0]) + 4056.1485662266955) < 1e-8

combined = chron[chron["sex"] == "Combined"].set_index("model")
assert combined.loc["RH", "rmse"] < combined.loc["LC", "rmse"]
assert combined.loc["RH", "rmse"] < combined.loc["APC", "rmse"]
assert combined.loc["RH", "rmse"] < combined.loc["CBD-LR", "rmse"]
assert combined.loc["RH-XGBOOST", "rmse"] > combined.loc["RH", "rmse"]

assert (diag["max_rhat"] < 1.01).all()
assert (diag["min_bulk_ess"] > 400).all()
assert (diag["min_tail_ess"] > 400).all()
assert (diag["divergences"] == 0).all()
assert (diag["treedepth_hits"] == 0).all()

assert int(e0["year"].max()) == 2040
assert int(rates["year"].max()) == 2040
assert float(srs.loc[(srs.sex == "Female") & (srs.period == "2016-20"), "absolute_difference_years"].iloc[0]) > 6

stan_text = (ROOT / "stan/cbd_lr.stan").read_text(encoding="utf-8")
assert "CBD-inspired log-rate benchmark" in stan_text
assert "neg_binomial_2_log" in stan_text

print("PASS: repository files, model labels, headline results, diagnostics, and 2040 horizon are consistent.")

