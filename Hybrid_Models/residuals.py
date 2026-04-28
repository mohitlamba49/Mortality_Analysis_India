def compute_residuals(data, rh_pred):
    df = prepare_features(data)
    residual = log(mx) - log(rh_pred)
    return df_with_residual
