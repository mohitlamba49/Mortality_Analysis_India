def main():

    ensure_cmdstan()

    # Load data
    data, sex_labels = load_input_data()

    # Prepare data
    rh_data, rh_levels = prepare_rh_data(data)

    # Fit model
    rh_model, rh_fit = fit_stan_model(...)

    # Diagnostics
    diagnostic_plots(rh_fit)

    # Posterior analysis
    extract posterior means
    plot results

    # Fit quality
    fitted_df = compute_fitted_values(...)
    posterior_predictive_checks(...)

    # Validation
    out_of_sample_validation(...)

    # Forecast
    table_data, life_exp, forecast_df, fan_df = run_forecasting(...)

    # Add uncertainty
    final_table = add_uncertainty(...)

    # Print/export results

END
