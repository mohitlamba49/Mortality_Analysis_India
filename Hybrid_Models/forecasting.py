def forecast_kappa(kappa, horizon):
    compute drift
    generate future kappa
    return kappa_future


def forecast_rh(fit, levels, data):
    forecast kappa
    compute future mortality using RH
    return future dataframe


def forecast_hybrid(xgb_model, data, rh_future):

    initialize historical data

    FOR each future time step:
        - extract previous mortality (lag)
        - create feature vector
        - predict residual
        - update mortality
        - append to history

    return hybrid forecast
