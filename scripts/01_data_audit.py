from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_FILE = ROOT / "results" / "validation" / "data_audit_rebuilt.csv"


def audit_panel(path, sex):
    frame = pd.read_excel(path)
    required = {"age_int", "year", "deaths", "Exposure"}
    missing_columns = required.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"{path.name}: missing columns {sorted(missing_columns)}")

    ages = sorted(frame["age_int"].unique())
    years = sorted(frame["year"].unique())
    expected = pd.MultiIndex.from_product([ages, years], names=["age_int", "year"])
    observed = pd.MultiIndex.from_frame(frame[["age_int", "year"]])

    return {
        "sex": sex,
        "rows": len(frame),
        "age_groups": len(ages),
        "first_year": int(min(years)),
        "last_year": int(max(years)),
        "missing_cells": int(len(expected.difference(observed))),
        "duplicate_age_year_cells": int(frame.duplicated(["age_int", "year"]).sum()),
        "non_positive_exposures": int((frame["Exposure"] <= 0).sum()),
        "negative_deaths": int((frame["deaths"] < 0).sum()),
        "total_deaths": int(frame["deaths"].sum()),
        "total_exposure": float(frame["Exposure"].sum()),
    }


audit = pd.DataFrame(
    [
        audit_panel(DATA_DIR / "male_mortality_2000_2016.xlsx", "Male"),
        audit_panel(DATA_DIR / "female_mortality_2000_2016.xlsx", "Female"),
    ]
)

if not (
    (audit["rows"] == 323).all()
    and (audit["age_groups"] == 19).all()
    and (audit["first_year"] == 2000).all()
    and (audit["last_year"] == 2016).all()
    and (audit["missing_cells"] == 0).all()
    and (audit["duplicate_age_year_cells"] == 0).all()
    and (audit["non_positive_exposures"] == 0).all()
    and (audit["negative_deaths"] == 0).all()
):
    raise AssertionError("The deposited estimation panels do not pass the manuscript audit.")

audit.to_csv(OUT_FILE, index=False)
print(audit.to_string(index=False))
print("\nPASS: complete 2000-2016 panels; no imputation or missing-data handling required.")

