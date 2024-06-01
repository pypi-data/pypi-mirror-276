import numpy as np
from sklearn.metrics import mean_absolute_error

##############################################################################################

def absolute_r2_score(y_true, y_pred):

    Y_test_hat_mean_model = np.repeat(np.mean(y_true), len(y_true))
    MAE_best_model = mean_absolute_error(y_pred=y_pred, y_true=y_true)
    MAE_mean_model = mean_absolute_error(y_pred=Y_test_hat_mean_model, y_true=y_true)
    absolute_r2_score = 1 - (MAE_best_model / MAE_mean_model)
    
    return absolute_r2_score

##############################################################################################