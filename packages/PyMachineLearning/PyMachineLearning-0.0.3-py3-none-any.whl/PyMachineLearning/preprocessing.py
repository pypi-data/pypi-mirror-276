################################################################################
import numpy as np
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, MinMaxScaler, KBinsDiscretizer, StandardScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
from sklearn.feature_selection import SelectFdr, SelectFpr, SelectKBest, SelectPercentile, f_regression, f_classif, mutual_info_classif, SequentialFeatureSelector
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA
                          
################################################################################

class imputer(BaseEstimator, TransformerMixin):

    def __init__(self, apply=True, method='simple_median', n_neighbors=4, n_nearest_features=4):
        self.apply = apply
        self.method = method
        self.n_neighbors = n_neighbors
        self.n_nearest_features = n_nearest_features

    def fit(self, X, y=None):

        if self.apply == True:

            if self.method in ['simple_mean', 'simple_median', 'simple_most_frequent']:
                 self.imputer_ = SimpleImputer(missing_values=np.nan, strategy='_'.join(self.method.split('_')[1:]))
            elif self.method == 'knn':
                 self.imputer_ = KNNImputer(n_neighbors=self.n_neighbors, weights="uniform")
            elif self.method in ['iterative_mean', 'iterative_median', 'iterative_most_frequent']:
                 # 'iterative_most_frequent' doesn't work as expected. It generates float values different from the uniques ones of the categorical variable on which it's applied.
                 self.imputer_ = IterativeImputer(initial_strategy='_'.join(self.method.split('_')[1:]), 
                                                  n_nearest_features=self.n_nearest_features, max_iter=25, random_state=123)
            else:
                 raise ValueError("Invalid method for imputation")
           
            self.imputer_.fit(X)
        return self

    def transform(self, X):
        
        if self.apply == True:
            X = self.imputer_.transform(X) # Output: numpy array
        return X

################################################################################
    
class encoder(BaseEstimator, TransformerMixin):

    def __init__(self, method='ordinal', drop='first'): # drop=None to not remove any dummy
        self.method = method
        self.drop = drop

    def fit(self, X, y=None):

        if self.method == 'ordinal':
            self.encoder_ = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
        elif self.method == 'one-hot':
            self.encoder_ = OneHotEncoder(drop=self.drop, handle_unknown='ignore', sparse_output=True)
        else:
            raise ValueError("Invalid method for encoding")
        
        self.encoder_.fit(X)
        return self

    def transform(self, X):
        
        if self.method == 'one-hot':
            # One-hot encoding gives an sparse matrix as output.
            # The output is transformed from sparse to dense matrix since this is usually required in sklearn.
            X = self.encoder_.transform(X).toarray() 
        else: 
            X = self.encoder_.transform(X)


        return X
    
################################################################################
    
class scaler(BaseEstimator, TransformerMixin):

    def __init__(self, apply=False, method='standard'):
        
        self.apply = apply
        self.method = method

    def fit(self, X, y=None):
        
        if self.apply == True:
            if self.method == 'standard':
                self.scaler_ = StandardScaler(with_mean=True, with_std=True)
            elif self.method == 'min-max':
                self.scaler_ = MinMaxScaler(feature_range=(0, 1))
            self.scaler_.fit(X)

        return self
    
    def transform(self, X):
        
        if self.apply == True:
            X = self.scaler_.transform(X)
        return X 
    
################################################################################
    
class discretizer(BaseEstimator, TransformerMixin):

    def __init__(self, apply=False, n_bins=3, strategy='quantile'):
        self.apply = apply
        self.n_bins = n_bins
        self.strategy = strategy

    def fit(self, X, y=None):
        
        if self.apply == True:
            self.discretizer_ = KBinsDiscretizer(encode='ordinal', n_bins=self.n_bins, strategy=self.strategy)
            self.discretizer_.fit(X)
        return self
    
    def transform(self, X):
        
        if self.apply == True:
            X = self.discretizer_.transform(X)
        return X 
    
################################################################################
    
class features_selector(BaseEstimator, TransformerMixin):

    def __init__(self, apply=False, method='Fdr', cv=3, k=5, percentile=50, n_neighbors=7, alpha=0.05, n_jobs=None):
        self.apply = apply
        self.method = method
        self.cv = cv # number of folds in cross_val_score for forward/backward algorithms.
        self.k = k # number of features to keep in SelectKBest. 
        self.percentile = percentile # percent of features to keep in SelectPercentile.
        self.n_neighbors = n_neighbors # used in forward/backward KNN.
        self.alpha = alpha
        self.n_jobs = n_jobs

    def fit(self, X, y):
        
        if self.apply == True:

            if self.method == 'Fdr_f_reg':
                self.features_selector_ = SelectFdr(f_regression, alpha=self.alpha)
            elif self.method == 'Fpr_f_reg':
                self.features_selector_ = SelectFpr(f_regression, alpha=self.alpha)
            elif self.method == 'KBest_f_reg':
                self.features_selector_ = SelectKBest(f_regression, k=self.k)
            elif self.method == 'Percentile_f_reg':
                self.features_selector_ = SelectPercentile(f_regression, percentile=self.percentile)  
            elif self.method == 'Fdr_f_class':
                self.features_selector_ = SelectFdr(f_classif, alpha=self.alpha)
            elif self.method == 'Fpr_f_class':
                self.features_selector_ = SelectFpr(f_classif, alpha=self.alpha)
            elif self.method == 'KBest_f_class':
                self.features_selector_ = SelectKBest(f_classif, k=self.k)
            elif self.method == 'Percentile_f_class':
                self.features_selector_ = SelectPercentile(f_classif, percentile=self.percentile)  
            elif self.method == 'KBest_mutual_class':
                self.features_selector_ = SelectKBest(mutual_info_classif, k=self.k)
            elif self.method == 'Percentile_mutual_class':
                self.features_selector_ = SelectPercentile(mutual_info_classif, percentile=self.percentile)

            elif self.method == 'forward_linear_reg':
                self.features_selector_ = SequentialFeatureSelector(estimator=LinearRegression(),
                                                                    n_features_to_select='auto',
                                                                    direction='forward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'backward_linear_reg':
                self.features_selector_ = SequentialFeatureSelector(estimator=LinearRegression(),
                                                                    n_features_to_select='auto',
                                                                    direction='backward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'forward_knn_reg':
                self.features_selector_ = SequentialFeatureSelector(estimator=KNeighborsRegressor(n_neighbors=self.n_neighbors),
                                                                    n_features_to_select='auto',
                                                                    direction='forward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'backward_knn_reg':
                self.features_selector_ = SequentialFeatureSelector(estimator=KNeighborsRegressor(n_neighbors=self.n_neighbors),
                                                                    n_features_to_select='auto',
                                                                    direction='backward', cv=self.cv, n_jobs=self.n_jobs) 
            elif self.method == 'forward_knn_class':
                self.features_selector_ = SequentialFeatureSelector(estimator=KNeighborsClassifier(n_neighbors=self.n_neighbors),
                                                                    n_features_to_select='auto',
                                                                    direction='forward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'backward_knn_class':
                self.features_selector_ = SequentialFeatureSelector(estimator=KNeighborsClassifier(n_neighbors=self.n_neighbors),
                                                                    n_features_to_select='auto',
                                                                    direction='backward', cv=self.cv, n_jobs=self.n_jobs) 
            elif self.method == 'forward_logistic':
                self.features_selector_ = SequentialFeatureSelector(estimator=LogisticRegression(),
                                                                    n_features_to_select='auto',
                                                                    direction='forward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'backward_logistic':
                self.features_selector_ = SequentialFeatureSelector(estimator=LogisticRegression(),
                                                                    n_features_to_select='auto',
                                                                    direction='backward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'backward_trees_class':
                self.features_selector_ = SequentialFeatureSelector(estimator=DecisionTreeClassifier(max_depth=4),
                                                                    n_features_to_select='auto',
                                                                    direction='backward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'forward_trees_class':
                self.features_selector_ = SequentialFeatureSelector(estimator=DecisionTreeClassifier(max_depth=4),
                                                                    n_features_to_select='auto',
                                                                    direction='forward', cv=self.cv, n_jobs=self.n_jobs)
            else:
                raise ValueError("Invalid method for features selector")
        
            self.features_selector_.fit(X, y)
        
        return self
    
    def transform(self, X):
        
        if self.apply == True:
            X = self.features_selector_.transform(X)
        return X  
    
################################################################################

class pca(BaseEstimator, TransformerMixin):

    def __init__(self, apply=False, n_components=2, random_state=123):
        
        self.apply = apply
        self.n_components = n_components
        self.random_state = random_state

    def fit(self, X, y=None):
        
        if self.apply == True:
            self.PCA_ = PCA(n_components=self.n_components, random_state=self.random_state)
            self.PCA_.fit(X)

        return self
    
    def transform(self, X):
        
        if self.apply == True:
            X = self.PCA_.transform(X)
        return X 

################################################################################
    

################################################################################
    

################################################################################
    

################################################################################
    

################################################################################
    

################################################################################