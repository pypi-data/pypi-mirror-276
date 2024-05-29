from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, AdaBoostRegressor, ExtraTreesRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.svm import SVR
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error, median_absolute_error, r2_score
from sklearn.model_selection import cross_val_score, GridSearchCV
import numpy as np


def gb_regression(X_train, X_test, y_train, y_test):
    """
    Eng: Function for training and evaluating the GradientBoostingRegressor model.
    Fra: Fonction pour entraîner et évaluer le modèle GradientBoostingRegressor.
    Rus: Функция для обучения и оценки модели GradientBoostingRegressor.
    Ger: Funktion zum Trainieren und Evaluieren des GradientBoostingRegressor-Modells.

    Parameters:
    X_train: Training feature dataset
    X_test: Testing feature dataset
    y_train: Training target variable dataset
    y_test: Testing target variable dataset

    Returns:
    dict: Dictionary with model evaluations (MAE, MSE, RMSE, R^2)
    """
    gb_model = GradientBoostingRegressor(random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred = gb_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    results = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2
    }
    
    return results, gb_model

def rf_regression(X_train, X_test, y_train, y_test):
    """
    Eng: Function for training and evaluating the RandomForestRegressor model.
    Fra: Fonction pour entraîner et évaluer le modèle RandomForestRegressor.
    Rus: Функция для обучения и оценки модели RandomForestRegressor.
    Ger: Funktion zum Trainieren und Evaluieren des RandomForestRegressor-Modells.

    Parameters:
    X_train: training sample of features
    X_test: test sample of features
    y_train: training sample of the target variable
    y_test: test selection of the target variable

    Returns:
    dict: Dictionary with model estimates (MAE, MSE, MSU, R^2)
    """
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    results = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2
    }
    
    return results, rf_model

def lr_regression(X_train, X_test, y_train, y_test):
    """
    Eng: Function for training and evaluating the LinearRegression model.
    Fra: Fonction pour entraîner et évaluer le modèle LinearRegression.
    Rus: Функция для обучения и оценки модели LinearRegression.
    Ger: Funktion zum Trainieren und Evaluieren des LinearRegression-Modells.

    Parameters:
    X_train: training sample of features
    X_test: test sample of features
    y_train: training sample of the target variable
    y_test: test selection of the target variable

    Returns:
    dict: Dictionary with model estimates (MAE, MSE, MSU, R^2)
    """
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred = lr_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    results = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2
    }
    
    return results, lr_model

def catboost_regression(X_train, X_test, y_train, y_test):
    """
    Eng: Function for training and evaluating the CatBoostRegressor model.
    Fra: Fonction pour entraîner et évaluer le modèle CatBoostRegressor.
    Rus: Функция для обучения и оценки модели CatBoostRegressor.
    Ger: Funktion zum Trainieren und Evaluieren des CatBoostRegressor-Modells.

    Parameters:
    X_train: training sample of features
    X_test: test sample of features
    y_train: training sample of the target variable
    y_test: test selection of the target variable

    Returns:
    dict: Dictionary with model estimates (MAE, MSE, MSU, R^2)
    """
    catboost_model = CatBoostRegressor(iterations=1000, depth=6, learning_rate=0.1, loss_function='RMSE', random_state=42)
    catboost_model.fit(X_train, y_train, verbose=100)
    y_pred = catboost_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    results = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2
    }
    
    return results, catboost_model

def xgb_regression(X_train, X_test, y_train, y_test):
    """
    Eng: Function for training and evaluating the XGBRegressor model.
    Fra: Fonction pour entraîner et évaluer le modèle XGBRegressor.
    Rus: Функция для обучения и оценки модели XGBRegressor.
    Ger: Funktion zum Trainieren und Evaluieren des XGBRegressor-Modells.

    Parameters:
    X_train: training sample of features
    X_test: test sample of features
    y_train: training sample of the target variable
    y_test: test selection of the target variable

    Returns:
    dict: Dictionary with model estimates (MAE, MSE, MSU, R^2)
    """
    xgb_model = XGBRegressor(random_state=42)
    xgb_model.fit(X_train, y_train)
    y_pred = xgb_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    results = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2
    }
    
    return results, xgb_model

def cross_val_evaluate(model, X, y, cv=5, scoring='neg_mean_squared_error'):
    """
    Eng: Function for cross-validation of the model.
    Fra: Fonction pour la validation croisée du modèle.
    Rus: Функция для кросс-валидации модели.
    Ger: Funktion für die Kreuzvalidierung des Modells.

    Parameters:
    Model: Regression Modeler
    X: a selection of acquaintances
    y: a sample of a parallel time
    summary: a team for cross-validation (5 in total)
    scoring: the oshenka method (by mistake 'neg_mean_squared_error')

    Returns:
    dictation: A dictionary with the words "Done" (ROSE per fold, Man RISE)
    """
    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
    rmse_scores = np.sqrt(-scores)
    
    model.fit(X, y)
    
    results = {
        'RMSE per fold': rmse_scores,
        'Mean RMSE': rmse_scores.mean()
    }
    
    return results, model


def optimize_model(model_name, model, X_train, y_train, X_test, y_test, cv=5, scoring='neg_mean_squared_error'):
    """
    Eng: Function for hyperparameter optimization of the model using GridSearchCV and model evaluation after optimization.
    Fra: Fonction pour l'optimisation des hyperparamètres du modèle en utilisant GridSearchCV et l'évaluation du modèle après l'optimisation.
    Rus: Функция для оптимизации гиперпараметров модели с использованием GridSearchCV и оценки модели после оптимизации.
    Ger: Funktion zur Optimierung der Hyperparameter des Modells unter Verwendung von GridSearchCV und Bewertung des Modells nach der Optimierung.

    Parameters:
    model_name: The name of the model (used to select parameters from param_grids)
    model: Regression model
    X_train: training sample of features
    y_train: training sample of the target variable
    X_test: test sample of features
    y_test: test sample of target variable
    cv: number of folds for cross validation (default 5)
    scoring: evaluation method (default 'neg_mean_squared_error')

    Returns:
    dict: The best model and its parameters, as well as model estimates after optimization
    """
    param_grids = {
        'GradientBoostingRegressor': {
            'n_estimators': [100, 200, 300],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [3, 4, 5]
        },
        'RandomForestRegressor': {
            'n_estimators': [100, 200, 300],
            'max_features': ['auto', 'sqrt', 'log2'],
            'max_depth': [10, 20, 30]
        },
        'LinearRegression': {
            'fit_intercept': [True, False],
            'normalize': [True, False]
        },
        'CatBoostRegressor': {
            'iterations': [500, 1000, 1500],
            'depth': [4, 6, 8],
            'learning_rate': [0.01, 0.1, 0.2]
        },
        'XGBRegressor': {
            'n_estimators': [100, 200, 300],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [3, 4, 5]
        }
    }

    param_grid = param_grids[model_name]
    grid_search = GridSearchCV(model, param_grid, cv=cv, scoring=scoring)
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_

    y_pred = best_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    results = {
        'Best Parameters': best_params,
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2
    }
    
    return results, best_model