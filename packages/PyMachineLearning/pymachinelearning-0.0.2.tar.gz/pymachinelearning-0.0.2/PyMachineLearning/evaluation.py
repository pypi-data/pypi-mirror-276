################################################################################

import numpy as np
from sklearn.model_selection import cross_val_score, RandomizedSearchCV, PredefinedSplit, GridSearchCV
import polars as pl
import pandas as pd
import numpy as np
import optuna

################################################################################

class OptunaSearchCV:
    
    def __init__(self, estimator, param_grid, cv, scoring, direction='minimize', n_iter=10, random_state=123, groups=None, framework=None, input_dim=1, output_dim=1):

        self.estimator = estimator
        self.param_grid = param_grid
        self.cv = cv
        self.scoring = scoring
        self.direction = direction
        self.n_iter = n_iter
        self.random_state = random_state
        self.groups = groups
        self.framework = framework
        self.input_dim = input_dim
        self.output_dim = output_dim

    def objective(self, trial, X, y):
       
       if self.framework == 'PyTorch':
            self.estimator.set_params(**self.param_grid(trial, self.input_dim, self.output_dim))
       else:
            self.estimator.set_params(**self.param_grid(trial))
       score = np.mean(cross_val_score(X=X, y=y, estimator=self.estimator, scoring=self.scoring, cv=self.cv, groups=self.groups))
       return score 
    
    def fit(self, X, y):
       
       sampler = optuna.samplers.TPESampler(seed=self.random_state)
       study = optuna.create_study(direction=self.direction, sampler=sampler)
       study.optimize(lambda trial: self.objective(trial, X=X, y=y), n_trials=self.n_iter) 
       self.best_params_ = study.best_params
       self.best_score_ = study.best_value 
       self.study = study

    def results(self):
          # Collect trial information
        results = []
        for trial in self.study.trials:
            trial_data = {
              'params': trial.params,
              'score': trial.value,
              'time': trial.duration.total_seconds()
              }
            results.append(trial_data)

        # Create a DataFrame from the collected information
        results = pd.DataFrame(results)
        results = pd.concat((results['params'].apply(lambda x: pd.Series(x)), results[['score', 'time']]), axis=1)
        if self.direction == 'maximize':
            results = results.sort_values(by='score', ascending=False)
        elif self.direction == 'minimize':
            results = results.sort_values(by='score', ascending=True)
        return results
    
################################################################################

def optuna_nested_results(search, estimator, inner_results, outer_scores, metric, X_train, X_test, Y_train, Y_test):

    # Inner results (HPO)
    inner_results.append(search.results())
    # Outer score (estimation future performance)
    best_estimator = estimator.set_params(**search.best_params_)
    best_estimator.fit(X_train, Y_train)
    Y_test_hat = best_estimator.predict(X_test)
    outer_scores.append(metric(y_true=Y_test, y_pred=Y_test_hat))

    return inner_results, outer_scores

################################################################################

def format_results(search, direction):

    results = pl.DataFrame(search.cv_results_)
    columns_to_keep = [x for x in results.columns if 'param' in x and x != 'params'] + ['mean_test_score']
    results = results[columns_to_keep]
    if direction == 'maximize':
        results = results.sort(by='mean_test_score', descending=True)
    elif direction == 'minimize':
        results = results.sort(by='mean_test_score', descending=False)
    rename_columns = ['_'.join(x.split('_')[1:]) for x in columns_to_keep[:(len(columns_to_keep)-1)]]
    rename_columns = rename_columns + ['score']
    results.columns = rename_columns
    return results

################################################################################

# A function that is used in SemiNested Evaluation
def predefine_split(data_size=None, train_prop=None, random=None, random_state=None, train_indices=None, test_indices=None):
    
    if None in [train_indices, test_indices]:
        train_size = round(train_prop*data_size)
        test_size = data_size - train_size
        train_indices = np.repeat(-1, train_size) # -1 = Train 
        test_indices = np.repeat(0, test_size)  # 0 = Test 
        indices = np.concatenate((train_indices, test_indices))
        if random == True:
            np.random.seed(random_state)
            indices = np.random.choice(indices, len(indices), replace=False)
    else:
        train_size = len(train_indices) ; test_size = len(test_indices)
        indices = np.zeros(train_size + test_size)
        indices[train_indices] = -1
    
    return PredefinedSplit(indices)

# Examples of usage
# predefine_split(data_size=len(X_train), train_prop=0.75, random=True, random_state=123)
# predefine_split(data_size=len(X), train_prop=0.75, random=False)
# predefine_split(train_indices=[0,2,3,5,10], test_indices=[1,4,6,7,8,9])

################################################################################

class SimpleEvaluation: # Outer: Simple Validation ; Inner: Simple or CV

    def __init__(self, estimator, param_grid, cv, search_method, scoring, direction='minimize', n_trials=10, 
                 groups=None, random_state=123, framework=None, input_dim=1, output_dim=1):
            
        self.estimator = estimator
        self.param_grid = param_grid
        self.cv = cv
        self.search_method = search_method
        self.scoring = scoring
        self.direction = direction
        self.n_trials = n_trials
        self.random_state = random_state
        self.framework = framework
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.groups = groups
    
    def fit(self, X, y):
            
        # Inner HPO
        if self.search_method == 'optuna':

            search = OptunaSearchCV(estimator=self.estimator, param_grid=self.param_grid,       
                                    cv=self.cv, groups=self.groups, scoring=self.scoring, direction=self.direction,
                                    n_iter=self.n_trials, random_state=self.random_state,
                                    framework=self.framework, input_dim=self.input_dim, output_dim=self.output_dim)
            
        else:

            if self.search_method == 'random_search':              
                search = RandomizedSearchCV(estimator=self.estimator, param_distributions=self.param_grid, 
                                            cv=self.cv, scoring=self.scoring, 
                                            n_iter=self.n_trials, random_state=self.random_state)

            elif self.search_method == 'grid_search':              

                search = GridSearchCV(estimator=self.estimator, param_grid=self.param_grid, 
                                      cv=self.cv, scoring=self.scoring)          
            
        search.fit(X, y)
        # Inner results (HPO)
        self.inner_results = search.results() if self.search_method == 'optuna' else format_results(search, self.direction)
        # Inner score  
        self.inner_score = search.best_score_
        # Inner best params
        self.inner_best_params = search.best_params_

################################################################################

class NestedEvaluation: # Outer: CV ; Inner: CV

    def __init__(self, estimator,  cv, outer, scoring, metric, direction='minimize', param_grid=None, search_method=None, n_trials=10, random_state=123):
         
        self.estimator = estimator
        self.param_grid = param_grid
        self.cv = cv
        self.outer = outer
        self.search_method = search_method
        self.scoring = scoring
        self.metric = metric # must be a sklearn.metric function according to scoring name
        self.direction = direction
        self.n_trials = n_trials  
        self.random_state = random_state      

    def fit(self, X, y):

        inner_scores, outer_scores, inner_best_params, inner_results = [], [], [], []

        for k, (train_index, test_index) in enumerate(self.outer.split(X)) :
            
            print('----------------')
            print(f'Outer: Fold {k+1}')
            print('----------------')
            if isinstance(X, pd.DataFrame):
                X_train, X_test = X.iloc[train_index,:], X.iloc[test_index,:]
            elif isinstance(X, np.ndarray):
                X_train, X_test = X[train_index,:], X[test_index,:]
            Y_train, Y_test = Y[train_index], Y[test_index]

            if self.search_method is None:
                
                inner_score = np.mean(cross_val_score(estimator=self.estimator, X=X_train, y=Y_train, scoring=self.scoring, cv=self.cv))
                inner_score = -inner_score if 'neg' in self.scoring else inner_score
                inner_scores.append(inner_score)
                self.estimator.fit(X=X_train, y=Y_train)
                Y_test_hat = self.estimator.predict(X_test)
                outer_scores.append(self.scoring(y_true=Y_test, y_pred=Y_test_hat))

            else:

                # Inner HPO
                if self.search_method == 'optuna':

                    search = OptunaSearchCV(estimator=self.estimator, param_grid=self.param_grid, 
                        cv=self.cv, scoring=self.scoring, direction=self.direction, n_iter=self.n_trials, seed=self.random_state)
                    search.fit(X_train, Y_train)
                    
                    inner_results, outer_scores = optuna_nested_results(search, self.estimator, inner_results, outer_scores, self.metric, X_train, X_test, Y_train, Y_test)

                else:
                    
                    if self.search_method == 'random_search':
                
                        search = RandomizedSearchCV(estimator=self.estimator, param_distributions=self.param_grid, 
                                cv=self.cv, scoring=self.scoring, n_iter=self.n_trials, random_state=self.random_state)
                        search.fit(X_train, Y_train)

                    elif self.search_method == 'grid_search':              

                        search = GridSearchCV(estimator=self.estimator, param_grid=self.param_grid, 
                                                cv=self.cv, scoring=self.scoring)  
                    
                    # Inner results (HPO)
                    inner_results.append(format_results(search, self.direction))
                    # Outer score (estimation future performance)
                    outer_scores.append(search.score(X=X_test, y=Y_test))                   
            
                # Inner (HPO) best_params and score
                inner_best_params.append(search.best_params_)
                inner_scores.append(search.best_score_)

        self.inner_results = inner_results
        self.inner_best_params = inner_best_params
        self.outer_scores = np.array(outer_scores)
        self.inner_scores = np.array(inner_scores)
        self.final_inner_score = np.mean(self.inner_scores)
        self.final_outer_score = np.mean(self.outer_scores) # Estimation of future performance
        # The one with the least MAE. This is a criteria to obtain the finals params, but not the only possible.
        if self.search_method is not None:
            self.final_best_params = inner_best_params[np.argmin(self.inner_scores)]

################################################################################

class SemiNestedEvaluation: # Outer: CV ; Inner: Simple

    def __init__(self, estimator, param_grid, outer, search_method, scoring, direction='maximize', n_trials=10, 
                 random_state=123, train_prop=0.75, random_sv=True, train_indices=None, test_indices=None):
        self.estimator = estimator
        self.param_grid = param_grid
        self.outer = outer
        self.search_method = search_method
        self.scoring = scoring
        self.direction = direction
        self.n_trials = n_trials
        self.random_state = random_state
        self.train_prop = train_prop
        self.random_sv = random_sv
        self.train_indices = train_indices
        self.test_indices = test_indices
    
    def fit(self, X, y):

        inner_scores, outer_scores, inner_best_params, inner_results = [], [], [], []

        for k, (train_index, test_index) in enumerate(self.outer.split(X)) :
            
            print('----------------')
            print(f'Outer: Fold {k+1}')
            print('----------------')
            if isinstance(X, pd.DataFrame):
                X_train, X_test = X.iloc[train_index,:], X.iloc[test_index,:]
            elif isinstance(X, np.ndarray):
                X_train, X_test = X[train_index,:], X[test_index,:]
            Y_train, Y_test = Y[train_index], Y[test_index]

            # Inner definition (differential step)
            self.cv = predefine_split(data_size=len(X_train), train_prop=self.train_prop, random=self.random_sv, 
                                    random_state=self.random_state, train_indices=self.train_indices, test_indices=self.test_indices)
            # Inner HPO
            if self.search_method == 'optuna':

                search = OptunaSearchCV(estimator=self.estimator, param_grid=self.param_grid, 
                    cv=self.cv, scoring=self.scoring, direction=self.direction, n_iter=self.n_trials, seed=self.random_state)
                search.fit(X_train, Y_train)
                
                inner_results, outer_scores = optuna_nested_results(search, self.estimator, inner_results, outer_scores, self.scoring, X_train, X_test, Y_train, Y_test)

            else:
                
                if self.search_method == 'random_search':
            
                    search = RandomizedSearchCV(estimator=self.estimator, param_distributions=self.param_grid, 
                            cv=self.cv, scoring=self.scoring, n_iter=self.n_trials, random_state=self.random_state)
                    search.fit(X_train, Y_train)

                elif self.search_method == 'grid_search':              

                    search = GridSearchCV(estimator=self.estimator, param_grid=self.param_grid, 
                                            cv=self.cv, scoring=self.scoring)  
                
                # Inner results (HPO)
                inner_results.append(format_results(search, self.direction))
                # Outer score (estimation future performance)
                outer_scores.append(search.score(X=X_test, y=Y_test))                   
        
            # Inner (HPO) best_params and score
            inner_best_params.append(search.best_params_)
            inner_scores.append(search.best_score_)

        self.inner_results = inner_results
        self.inner_best_params = inner_best_params
        self.outer_scores = np.array(outer_scores)
        self.inner_scores = np.array(inner_scores)
        self.final_inner_score = np.mean(self.inner_scores)
        self.final_outer_score = np.mean(self.outer_scores) # Estimation of future performance
        # The one with the least MAE. This is a criteria to obtain the finals params, but not the only possible.
        self.final_best_params = inner_best_params[np.argmin(self.inner_scores)]

################################################################################
        
