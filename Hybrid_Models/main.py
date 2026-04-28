def run_full_pipeline(data):

    # STEP 1: RH MODEL
    rh_fit, levels = fit_rh_model(data)
    rh_pred = predict_rh(rh_fit, data, levels)

    # STEP 2: EVALUATE RH
    compute MAE, RMSE

    # STEP 3: RESIDUAL MODEL
    df_res = compute_residuals(data, rh_pred)

    # STEP 4: XGBOOST
    xgb_model = fit_xgb_residual_tuned(df_res)

    # STEP 5: HYBRID
    hybrid_pred = predict_hybrid(xgb_model, data, rh_pred)

    # STEP 6: COMPARISON
    compare RH vs Hybrid

    RETURN models


def generate_paper_results():

    # RH forecast
    rh_future = forecast_rh(...)

    # Hybrid forecast
    hybrid_future = forecast_hybrid(...)

    # Tables
    table1 = build_table(hybrid_future)

    # Metrics
    metrics = compute_metrics_by_sex(...)

    # Life expectancy
    life = compute_life_expectancy(...)
    combined = compute_combined_life_expectancy(...)

    print all outputs
