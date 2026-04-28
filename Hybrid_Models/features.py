def prepare_features(data):
    compute mx and log(mx)
    create lag feature (mx_lag1)
    scale year and cohort
    create interaction (age × year)
    return dataframe


def transform_future_features(df, original_data):
    apply same scaling
    return transformed features
