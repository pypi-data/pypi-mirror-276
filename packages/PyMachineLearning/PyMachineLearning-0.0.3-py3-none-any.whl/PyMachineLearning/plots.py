################################################################################
import numpy as np
import sys
import polars as pl
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('whitegrid')

sys.path.insert(0, r"C:\Users\fscielzo\Documents\Packages\PyMachineLearning_Package_Private")
from PyMachineLearning.metrics import absolute_r2_score

################################################################################

def predictive_plots(Y, Y_hat, Y_cat=None, model_name=None, future_performance=None, score_name=None, n_random_samples=50, random_state=123):

    if isinstance(Y, (pd.Series, pl.Series)):
        Y = Y.to_numpy()

    # Create an array of x-axis values
    np.random.seed(random_state)
    idx = np.arange(len(Y))
    random_idx = np.random.choice(idx, n_random_samples, replace=False)
    print(f'Estimation of future performance: \n{score_name} = {np.round(future_performance, 3)}')
    print(f'Absolute R2 = {np.round(absolute_r2_score(y_pred=Y_hat, y_true=Y), 3) * 100} %')

    # Plot 1: True values vs. Predicted values
    fig, axes = plt.subplots(figsize=(15, 6))
    ax = sns.scatterplot(y=Y_hat, x=Y, label='Predicted vs True', color='blue')
    ax = sns.regplot(x=Y, y=Y, scatter=False, 
                line_kws={'linestyle':'--', 'color':'red'}, 
                label='Perfect Fit')
    ax.set_xlabel('True Values')
    ax.set_ylabel('Predicted Values')
    ax.legend()
    ax.set_title(f'Predicted vs True Values - {model_name}', fontsize=15)
    plt.tight_layout()
    plt.show()
    
    # Plot 2: True values vs. Predicted values with data points selected randomly
    fig, ax = plt.subplots(figsize=(15, 5))
    ax = sns.scatterplot(y=Y_hat[random_idx], x=Y[random_idx], label='Predicted vs True', color='blue')
    ax = sns.regplot(x=Y[random_idx], y=Y[random_idx], scatter=False, 
                line_kws={'linestyle':'--', 'color':'red'}, 
                label='Perfect Fit')
    ax.set_xlabel('True Values')
    ax.set_ylabel('Predicted Values')
    ax.legend()
    ax.set_title(f'Predicted vs True Values ({n_random_samples} random data points)  - {model_name}', fontsize=15)
    plt.tight_layout()
    plt.show()

    # Plot 3: Line plot of True vs. Predicted values with data points selected as random
    fig, ax = plt.subplots(figsize=(15, 5))
    ax = sns.lineplot(x=random_idx, y=Y[random_idx], color='red', label='True Values', marker='o', markersize=5)
    ax = sns.lineplot(x=random_idx, y=Y_hat[random_idx], color='blue', label='Predicted Values', marker='o', markersize=5)
    ax.legend()
    ax.set_xlabel('Index')
    ax.set_ylabel('Values')
    ax.set_title(f'True vs Predicted Values ({n_random_samples} random data points)  - {model_name}', fontsize=15)
    plt.tight_layout()
    plt.show()

    # Plot 4: Boxplot of True vs. Predicted values 
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.boxplot(y=Y_hat, x=Y_cat, color='orange')
    ax.set_xlabel('True values')
    ax.set_ylabel('Predicted values')
    ax.set_title(f'Boxplot - True vs Predicted Values - {model_name}', fontsize=15)
    plt.tight_layout()
    plt.show()

################################################################################
    
def predictive_intervals(estimator, B, X_train, Y_train, X_test, Y_test, Y_test_hat, n_points=50, random_state=123, model_name=None):

   Y_test_hat_b = np.zeros((len(Y_test),B))
   for j, b in enumerate(range(0, B)):
      np.random.seed(random_state + b)
      bootstrap_indices = np.random.choice(np.arange(0,len(Y_train)), len(Y_train), replace=True)
      X_train_b, Y_train_b = X_train.iloc[bootstrap_indices,:], Y_train.iloc[bootstrap_indices]
      try:
         estimator.fit(X_train_b, Y_train_b)
         Y_test_hat_b[:,j] = estimator.predict(X_test)
      except:
         pass

   sd_bootstrap = np.std(Y_test_hat_b, axis=1)
   PI_1 = Y_test_hat - sd_bootstrap
   PI_2 = Y_test_hat + sd_bootstrap

   fig, axes = plt.subplots(figsize=(18, 6))
   np.random.seed(random_state)
   random_data_indices = np.random.choice(np.arange(0, len(X_test)), n_points, replace=False)

   # Scatter plot for actual data points
   sns.scatterplot(x=random_data_indices, y=Y_test.iloc[random_data_indices], 
                   color='red', label='True values')

   # Line plot for predicted values
   sns.lineplot(x=random_data_indices, y=Y_test_hat[random_data_indices], 
                color='blue', label='predicted values', marker='o', markersize=5)

   # Add a shaded area for the predictive intervals
   plt.fill_between(np.sort(random_data_indices), PI_1[np.sort(random_data_indices)], PI_2[np.sort(random_data_indices)],
                    color='green', alpha=0.3)
   #sns.lineplot(x=random_data_indices, y=PI_1[random_data_indices], color='fuchsia', linestyle='--')
   #sns.lineplot(x=random_data_indices, y=PI_2[random_data_indices], color='orange', linestyle='--')
   plt.set_title(f'Prediction intervals and Predicted values vs. True Values ({n_points} random data points) - {model_name}', fontsize=15)
   plt.show()

   print(f'The percentage of true values within the prediction intervals is {np.mean([(x >= PI_1) and (x <= PI_2) for x in Y_test_hat[random_data_indices]])}')

################################################################################

# Boxplot for understanding better the prediction
# We assume that Y is a quantitative variable but we assume that Y_test has been categorized.



################################################################################
    