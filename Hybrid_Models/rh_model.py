def fit_rh_model(data):
    prepare stan_data
    write stan file
    compile model
    run MCMC sampling
    return fit, levels


def predict_rh(fit, data, levels):
    extract alpha, beta, kappa, gamma
    map indices
    compute log mortality
    return exp(log_rate)
