def forecast_kappa(kappa_series):
    fit ARIMA
    forecast future values
    return forecast


def generate_scenarios(kappa):
    baseline = kappa
    optimistic = kappa - shift
    pessimistic = kappa + shift
    epidemic = spike early years
    return all scenarios


def run_forecasting(data, fit, levels):
    forecast kappa
    extend gamma
    compute mortality forecasts
    simulate uncertainty using posterior draws
    return forecast tables
