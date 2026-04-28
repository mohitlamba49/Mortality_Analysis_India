def predict_hybrid(xgb_model, data, rh_pred):
    create features
    predict residuals
    combine with RH:
        log_final = log_rh + residual
    return exp(log_final)
