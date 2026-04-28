def fit_xgb_residual_tuned(df):

    define features X
    define target y (residual)

    initialize XGBoost model

    define hyperparameter space:
        n_estimators
        max_depth
        learning_rate
        subsample
        regularization

    perform RandomizedSearchCV

    return best_model
