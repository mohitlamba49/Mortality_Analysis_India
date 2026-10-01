from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "figure.dpi": 160,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    }
)

colours = {
    "Male": "#285f9e",
    "Female": "#b23b3b",
    "Combined": "#4f7f44",
    "RH": "#4f7f44",
    "LC": "#4c78a8",
    "APC": "#f28e2b",
    "CBD-LR": "#b45f93",
    "RH-XGBOOST": "#777777",
}


# Full-period ELPD comparison
full = pd.read_csv(ROOT / "results/full_period/combined_four_model_comparison.csv")
full = full.sort_values("elpd_loo")
fig, axis = plt.subplots(figsize=(7.8, 4.6))
axis.barh(full["model"], full["elpd_loo"], color=[colours[x] for x in full["model"]])
axis.errorbar(
    full["elpd_loo"],
    full["model"],
    xerr=full["elpd_se"],
    fmt="none",
    ecolor="black",
    capsize=3,
    linewidth=1,
)
axis.set_xlabel("Expected log predictive density (higher is better)")
axis.set_title("Full-period pointwise predictive adequacy")
axis.grid(axis="x", alpha=0.2)
fig.tight_layout()
fig.savefig(FIGURES / "four_model_elpd_comparison.png")
plt.close(fig)


# Observed versus fitted rates
cells = pd.read_csv(ROOT / "results/full_period/cell_level_fitted_rates.csv")
model_order = ["LC", "APC", "CBD-LR", "RH"]
fig, axes = plt.subplots(2, 2, figsize=(9.2, 8.2), sharex=True, sharey=True)
for axis, model in zip(axes.ravel(), model_order):
    part = cells[cells["model"] == model]
    for sex in ["Male", "Female"]:
        sex_part = part[part["sex"] == sex]
        axis.scatter(
            sex_part["observed_rate"],
            sex_part["posterior_mean_fitted_rate"],
            s=11,
            alpha=0.55,
            color=colours[sex],
            label=sex,
        )
    lower = min(part["observed_rate"].min(), part["posterior_mean_fitted_rate"].min())
    upper = max(part["observed_rate"].max(), part["posterior_mean_fitted_rate"].max())
    axis.plot([lower, upper], [lower, upper], color="black", linestyle="--", linewidth=0.8)
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_title(model)
    axis.grid(alpha=0.18)
axes[1, 0].set_xlabel("Observed central mortality rate")
axes[1, 1].set_xlabel("Observed central mortality rate")
axes[0, 0].set_ylabel("Posterior mean fitted rate")
axes[1, 0].set_ylabel("Posterior mean fitted rate")
axes[0, 0].legend(frameon=False)
fig.suptitle("Observed and fitted mortality rates, 2000–2016", y=1.01)
fig.tight_layout()
fig.savefig(FIGURES / "observed_vs_fitted_all_models.png")
plt.close(fig)


# RH residual heatmaps
rh = cells[cells["model"] == "RH"].copy()
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.7), sharey=True)
limit = float(np.quantile(np.abs(rh["residual_rate"]), 0.98))
for axis, sex in zip(axes, ["Male", "Female"]):
    grid = rh[rh["sex"] == sex].pivot(index="age_int", columns="year", values="residual_rate")
    image = axis.imshow(
        grid.to_numpy(),
        aspect="auto",
        origin="lower",
        cmap="RdBu_r",
        vmin=-limit,
        vmax=limit,
    )
    axis.set_title(sex)
    axis.set_xlabel("Calendar year")
    axis.set_xticks(np.arange(0, len(grid.columns), 4))
    axis.set_xticklabels(grid.columns[::4])
    axis.set_yticks(np.arange(len(grid.index)))
    axis.set_yticklabels(grid.index)
axes[0].set_ylabel("Lower age bound")
fig.colorbar(image, ax=axes, shrink=0.82, label="Observed minus fitted rate")
fig.suptitle("RH residual structure")
fig.savefig(FIGURES / "rh_residual_heatmaps.png")
plt.close(fig)


# Chronological comparison
chron = pd.read_csv(ROOT / "results/chronological/four_model_chronological_validation.csv")
chron = chron[chron["sex"] == "Combined"].sort_values("rmse")
fig, axis = plt.subplots(figsize=(8.4, 4.7))
x = np.arange(len(chron))
width = 0.37
axis.bar(x - width / 2, chron["mae"], width, color="#4c78a8", label="MAE")
axis.bar(x + width / 2, chron["rmse"], width, color="#f28e2b", label="RMSE")
axis.set_xticks(x)
axis.set_xticklabels(chron["model"])
axis.set_ylabel("Mortality-rate error")
axis.set_title("Chronological validation: train 2000–2012; test 2013–2016")
axis.grid(axis="y", alpha=0.2)
axis.legend(frameon=False)
fig.tight_layout()
fig.savefig(FIGURES / "chronological_model_comparison.png")
plt.close(fig)


# Observed rates and RH projections through 2040
male = pd.read_excel(ROOT / "data/male_mortality_2000_2016.xlsx")
female = pd.read_excel(ROOT / "data/female_mortality_2000_2016.xlsx")
forecast = pd.read_csv(ROOT / "results/forecasts/rh_age_specific_mortality_forecasts_to_2040.csv")
for frame in [male, female]:
    frame["rate"] = frame["deaths"] / frame["Exposure"]

selected_ages = [0, 20, 30, 60]
age_labels = {0: "Under age 1", 20: "Ages 20–24", 30: "Ages 30–34", 60: "Ages 60–64"}
fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.5), sharex=True)
for axis, age in zip(axes.ravel(), selected_ages):
    for sex, observed in [("Male", male), ("Female", female)]:
        obs = observed[observed["age_int"] == age].sort_values("year")
        future = forecast[(forecast["sex"] == sex) & (forecast["age_int"] == age)].sort_values("year")
        axis.plot(obs["year"], obs["rate"], "o-", ms=2.7, lw=1.3, color=colours[sex], label=sex + " observed")
        axis.plot(future["year"], future["rate_median"], "--", lw=1.7, color=colours[sex], label=sex + " RH")
        axis.fill_between(future["year"], future["rate_lower_95"], future["rate_upper_95"], color=colours[sex], alpha=0.12)
    axis.axvline(2016, color="black", ls=":", lw=1)
    axis.set_title(age_labels[age])
    axis.set_yscale("log")
    axis.grid(alpha=0.2)
axes[1, 0].set_xlabel("Calendar year")
axes[1, 1].set_xlabel("Calendar year")
axes[0, 0].set_ylabel("Central mortality rate (log scale)")
axes[1, 0].set_ylabel("Central mortality rate (log scale)")
axes[0, 0].legend(frameon=False, fontsize=8, ncol=2)
fig.suptitle("Observed mortality and conditional RH projections through 2040", y=1.01)
fig.tight_layout()
fig.savefig(FIGURES / "observed_forecast_to_2040.png")
plt.close(fig)


# Internal life-expectancy series and external benchmarks
history = pd.read_csv(ROOT / "results/forecasts/historical_life_expectancy.csv")
future = pd.read_csv(ROOT / "results/forecasts/life_expectancy_forecasts_to_2040.csv")
benchmarks = pd.read_csv(ROOT / "data/srs_benchmarks.csv")
fig, axis = plt.subplots(figsize=(9.2, 5.3))
for sex in ["Male", "Female", "Combined"]:
    hist = history[history["sex"] == sex].sort_values("year")
    fut = future[future["sex"] == sex].sort_values("year")
    axis.plot(hist["year"], hist["e0"], "o-", ms=2.5, lw=1.2, color=colours[sex], alpha=0.85)
    axis.plot(fut["year"], fut["e0_median"], "--", lw=1.9, color=colours[sex], label=sex)
    axis.fill_between(fut["year"], fut["e0_lower_95"], fut["e0_upper_95"], color=colours[sex], alpha=0.10)
for marker, period in [("D", "2014-2018"), ("s", "2016-2020")]:
    part = benchmarks[benchmarks["period"] == period]
    axis.scatter(
        part["comparison_year"],
        part["official_e0"],
        marker=marker,
        s=35,
        color=[colours[x] for x in part["sex"]],
        edgecolor="black",
        linewidth=0.4,
        zorder=5,
        label=f"SRS {period} benchmark",
    )
axis.axvline(2016, color="black", ls=":", lw=1)
axis.set_xlim(2000, 2040)
axis.set_xlabel("Calendar year")
axis.set_ylabel("Model-implied life expectancy at birth (years)")
axis.set_title("Internal life-table series, conditional projections, and SRS benchmarks")
axis.grid(alpha=0.2)
axis.legend(frameon=False, fontsize=8, ncol=2)
fig.tight_layout()
fig.savefig(FIGURES / "life_expectancy_context_to_2040.png")
plt.close(fig)

print(f"Rebuilt public figures in {FIGURES}")

