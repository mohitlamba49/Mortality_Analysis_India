def write_stan_model(path, code):
    save stan code to file
    return file_path


def fit_stan_model(file, data, params):
    compile model
    run MCMC sampling
    return fit_object


def extract_posterior_means(fit):
    extract alpha, beta, kappa, gamma
    return means
