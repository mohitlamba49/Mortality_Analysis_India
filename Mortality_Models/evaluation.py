def compute_mae_rmse(observed, predicted):
    return mae, rmse


def out_of_sample_validation(data, model):
    split into train/test
    fit model on train
    predict test
    compute MAE, RMSE
