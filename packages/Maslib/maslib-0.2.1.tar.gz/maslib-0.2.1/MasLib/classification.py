import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report, r2_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from catboost import CatBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
import xgboost as xgb

def print_metrics(y_test, y_pred):
    """
    Eng: Output of classification model metrics.
    Fra: Sortie des métriques du modèle de classification.
    Rus: Вывод метрик модели классификации.
    Ger: Ausgabe von Metriken des Klassifikationsmodells.

    Parameters:
    y_test (np.ndarray): True class labels.
    y_pred (np.ndarray): Predicted class labels.

    """
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')
    r2 = r2_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)

    print(f'Model accuracy: {accuracy}')
    print(f'Precision: {precision}')
    print(f'Recall: {recall}')
    print(f'F1 Score: {f1}')
    print(f'R2 Score: {r2}')
    print('Confusion Matrix:\n', conf_matrix)
    print('Classification Report:\n', classification_rep)

def classification_with_svc(X_train, X_test, y_train, y_test):
    """
    Eng: Classification using SVC (Support Vector Classifier).
    Fra: Classification en utilisant SVC (Support Vector Classifier).
    Rus: Классификация с использованием SVC (Support Vector Classifier).
    Ger: Klassifizierung mit SVC (Support Vector Classifier).

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    model = make_pipeline(StandardScaler(), SVC())
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print_metrics(y_test, y_pred)

def classification_with_random_forest(X_train, X_test, y_train, y_test,n_estimatorse=100, random_states=42):
    """
    Eng: Classification using Random Forest Classifier.
    Fra: Classification en utilisant le classificateur Random Forest.
    Rus: Классификация с использованием Random Forest Classifier.
    Ger: Klassifizierung mit dem Random Forest Classifier.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    model = RandomForestClassifier(n_estimators=n_estimatorse, random_state=random_states)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print_metrics(y_test, y_pred)

def classification_with_knn(X_train, X_test, y_train, y_test, n_neighbors=3):
    """
    Eng: Classification using K-Nearest Neighbors (KNN).
    Fra: Classification en utilisant K-Nearest Neighbors (KNN).
    Rus: Классификация с использованием метода ближайших соседей (K-Nearest Neighbors, KNN).
    Ger: Klassifizierung mit K-Nearest Neighbors (KNN).

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    n_neighbors (int): The number of neighbors for the KNN algorithm. By default: 3.
    """
    knn_classifier = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn_classifier.fit(X_train, y_train)
    y_pred = knn_classifier.predict(X_test)
    print_metrics(y_test, y_pred)

def classification_with_logistic_regression(X_train, X_test, y_train, y_test,random_states=42, max_iters=1000):
    """
    Eng: Classification using Logistic Regression.
    Fra: Classification en utilisant la régression logistique.
    Rus: Классификация с использованием логистической регрессии.
    Ger: Klassifizierung mit logistischer Regression.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    model = LogisticRegression(random_state=random_states, max_iter=max_iters)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print_metrics(y_test, y_pred)

def classification_with_naive_bayes(X_train, X_test, y_train, y_test):
    """
    Eng: Classification using Naive Bayes.
    Fra: Classification en utilisant Naive Bayes.
    Rus: Классификация с использованием наивного байесовского классификатора.
    Ger: Klassifizierung mit Naive Bayes.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    model = GaussianNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print_metrics(y_test, y_pred)

def classification_with_decision_tree(X_train, X_test, y_train, y_test,random_states=42):
    """
    Eng: Classification using Decision Tree Classifier.
    Fra: Classification en utilisant le classificateur d'arbre de décision.
    Rus: Классификация с использованием классификатора дерева решений.
    Ger: Klassifizierung mit Entscheidungsbaum-Classifier.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    model = DecisionTreeClassifier(random_state=random_states)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print_metrics(y_test, y_pred)

def classification_with_gradient_boosting(X_train, X_test, y_train, y_test,n_estimatorse=100, random_states=42):
    """
    Eng: Classification using Gradient Boosting Classifier.
    Fra: Classification en utilisant le classificateur de boosting de gradient.
    Rus: Классификация с использованием классификатора градиентного бустинга.
    Ger: Klassifizierung mit Gradient Boosting Classifier.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    model = GradientBoostingClassifier(n_estimators=n_estimatorse, random_state=random_states)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print_metrics(y_test, y_pred)

def classification_with_adaboost(X_train, X_test, y_train, y_test,n_estimatorse=100, random_states=42):
    """
    Eng: Classification using AdaBoost Classifier.
    Fra: Classification en utilisant le classificateur AdaBoost.
    Rus: Классификация с использованием классификатора AdaBoost.
    Ger: Klassifizierung mit AdaBoost Classifier.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    model = AdaBoostClassifier(n_estimators=n_estimatorse, random_state=random_states)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print_metrics(y_test, y_pred)

def optimize_svc(X_train, X_test, y_train, y_test):
    """
    Eng: Optimization of SVC (Support Vector Classifier) using GridSearchCV.
    Fra: Optimisation de SVC (Support Vector Classifier) en utilisant GridSearchCV.
    Rus: Оптимизация SVC (Support Vector Classifier) с использованием GridSearchCV.
    Ger: Optimierung des SVC (Support Vector Classifier) mit GridSearchCV.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    pipe = Pipeline([('scaler', StandardScaler()), ('svc', SVC())])
    param_grid = {
        'svc__C': [0.1, 1, 10],
        'svc__gamma': [0.1, 0.01],
        'svc__kernel': ['linear', 'rbf']
    }
    grid = GridSearchCV(pipe, param_grid, refit=True, verbose=2)
    grid.fit(X_train, y_train)
    y_pred = grid.predict(X_test)
    print_metrics(y_test, y_pred)
    print("The best options:", grid.best_params_)
    return grid.best_estimator_, grid.best_params_

def optimize_random_forest(X_train, X_test, y_train, y_test):
    """
    Eng: Optimization of Random Forest Classifier using RandomizedSearchCV.
    Fra: Optimisation du classificateur Random Forest en utilisant RandomizedSearchCV.
    Rus: Оптимизация классификатора Random Forest с использованием RandomizedSearchCV.
    Ger: Optimierung des Random Forest Classifier mit RandomizedSearchCV.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    param_distributions = {
        'n_estimators': [50, 100],
        'max_features': ['auto', 'sqrt'],
        'max_depth': [4, 6, 8],
        'criterion': ['gini', 'entropy']
    }
    rand_search = RandomizedSearchCV(RandomForestClassifier(), param_distributions, n_iter=10, refit=True, verbose=2, random_state=42)
    rand_search.fit(X_train, y_train)
    y_pred = rand_search.predict(X_test)
    print_metrics(y_test, y_pred)
    print("The best options:", rand_search.best_params_)
    return rand_search.best_estimator_, rand_search.best_params_

def optimize_knn(X_train, X_test, y_train, y_test):
    """
    Eng: Optimization of K-Nearest Neighbors (KNN) using GridSearchCV.
    Fra: Optimisation des K-Nearest Neighbors (KNN) en utilisant GridSearchCV.
    Rus: Оптимизация K-Nearest Neighbors (KNN) с использованием GridSearchCV.
    Ger: Optimierung von K-Nearest Neighbors (KNN) mit GridSearchCV.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    param_grid = {
        'n_neighbors': [3, 5],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan']
    }
    grid = GridSearchCV(KNeighborsClassifier(), param_grid, refit=True, verbose=2)
    grid.fit(X_train, y_train)
    y_pred = grid.predict(X_test)
    print_metrics(y_test, y_pred)
    print("The best options:", grid.best_params_)
    return grid.best_estimator_, grid.best_params_

def optimize_logistic_regression(X_train, X_test, y_train, y_test):
    """
    Eng: Optimization of Logistic Regression using GridSearchCV.
    Fra: Optimisation de la régression logistique en utilisant GridSearchCV.
    Rus: Оптимизация логистической регрессии с использованием GridSearchCV.
    Ger: Optimierung der logistischen Regression mit GridSearchCV.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    param_grid = {
        'penalty': ['l1', 'l2'],
        'C': [0.1, 1, 10],
        'solver': ['liblinear']
    }
    grid = GridSearchCV(LogisticRegression(max_iter=1000), param_grid, refit=True, verbose=2)
    grid.fit(X_train, y_train)
    y_pred = grid.predict(X_test)
    print_metrics(y_test, y_pred)
    print("The best options:", grid.best_params_)
    return grid.best_estimator_, grid.best_params_

def optimize_naive_bayes(X_train, X_test, y_train, y_test):
    """
    Eng: Optimization of Naive Bayes does not require GridSearchCV, as the model has no hyperparameters to tune.
    Fra: L'optimisation de Naive Bayes ne nécessite pas GridSearchCV, car le modèle n'a pas de hyperparamètres à ajuster.
    Rus: Оптимизация наивного байесовского классификатора не требует GridSearchCV, так как у модели нет гиперпараметров для настройки.
    Ger: Die Optimierung von Naive Bayes erfordert kein GridSearchCV, da das Modell keine Hyperparameter zur Feinabstimmung hat.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    model = GaussianNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print_metrics(y_test, y_pred)
    return model, {}

def optimize_decision_tree(X_train, X_test, y_train, y_test):
    """
    Eng: Optimization of Decision Tree Classifier using GridSearchCV.
    Fra: Optimisation du classificateur d'arbre de décision en utilisant GridSearchCV.
    Rus: Оптимизация классификатора дерева решений с использованием GridSearchCV.
    Ger: Optimierung des Entscheidungsbaum-Classifiers mit GridSearchCV.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    param_grid = {
        'criterion': ['gini', 'entropy'],
        'max_depth': [4, 6, 8],
        'min_samples_split': [2, 5]
    }
    grid = GridSearchCV(DecisionTreeClassifier(), param_grid, refit=True, verbose=2)
    grid.fit(X_train, y_train)
    y_pred = grid.predict(X_test)
    print_metrics(y_test, y_pred)
    print("The best options:", grid.best_params_)
    return grid.best_estimator_, grid.best_params_

def optimize_gradient_boosting(X_train, X_test, y_train, y_test):
    """
    Eng: Optimization of Gradient Boosting Classifier using GridSearchCV.
    Fra: Optimisation du classificateur de boosting de gradient en utilisant GridSearchCV.
    Rus: Оптимизация классификатора градиентного бустинга с использованием GridSearchCV.
    Ger: Optimierung des Gradient Boosting Classifiers mit GridSearchCV.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    param_grid = {
        'n_estimators': [100, 200],
        'learning_rate': [0.01, 0.1],
        'max_depth': [3, 5]
    }
    grid = GridSearchCV(GradientBoostingClassifier(), param_grid, refit=True, verbose=2)
    grid.fit(X_train, y_train)
    y_pred = grid.predict(X_test)
    print_metrics(y_test, y_pred)
    print("The best options:", grid.best_params_)
    return grid.best_estimator_, grid.best_params_

def optimize_adaboost(X_train, X_test, y_train, y_test):
    """
    Eng: Optimization of AdaBoost Classifier using GridSearchCV.
    Fra: Optimisation du classificateur AdaBoost en utilisant GridSearchCV.
    Rus: Оптимизация классификатора AdaBoost с использованием GridSearchCV.
    Ger: Optimierung des AdaBoost Classifiers mit GridSearchCV.

    Parameters:
    X_train (pd.DataFrame): Training data.
    X_test (pd.DataFrame): Test data.
    y_train (pd.Series): True class labels for training data.
    y_test (pd.Series): True class labels for test data.
    """
    param_grid = {
        'n_estimators': [50, 100],
        'learning_rate': [0.01, 0.1, 1]
    }
    grid = GridSearchCV(AdaBoostClassifier(), param_grid, refit=True, verbose=2)
    grid.fit(X_train, y_train)
    y_pred = grid.predict(X_test)
    print_metrics(y_test, y_pred)
    print("Лучшие параметры:", grid.best_params_)
    return grid.best_estimator_, grid.best_params_

def grid_search_optimization(model_name, X_train, y_train):
    param_grids = {
        'gradient_boosting': {
            'n_estimators': [100, 150, 200],
            'learning_rate': [0.1, 0.05, 0.01],
            'max_depth': [3, 4, 5]
        },
        'random_forest': {
            'n_estimators': [100, 150, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        },
        'linear_regression': {
            'fit_intercept': [True, False],
            'normalize': [True, False]
        },
        'ridge': {
            'alpha': [0.1, 1.0, 10.0]
        },
        'lasso': {
            'alpha': [0.1, 1.0, 10.0]
        },
        'catboost': {
            'iterations': [500, 1000],
            'depth': [4, 6, 8],
            'learning_rate': [0.1, 0.05, 0.01]
        },
        'decision_tree': {
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        },
        'svr': {
            'C': [0.1, 1.0, 10.0],
            'epsilon': [0.1, 0.2, 0.5]
        },
        'xgboost': {
            'n_estimators': [100, 200, 300],
            'learning_rate': [0.1, 0.05, 0.01],
            'max_depth': [3, 4, 5]
        }
    }

    models = {
        'gradient_boosting': GradientBoostingRegressor(random_state=42),
        'random_forest': RandomForestRegressor(random_state=42),
        'linear_regression': LinearRegression(),
        'ridge': Ridge(),
        'lasso': Lasso(),
        'catboost': CatBoostRegressor(random_state=42, silent=True),
        'decision_tree': DecisionTreeRegressor(random_state=42),
        'svr': SVR(),
        'xgboost': xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    }

    if model_name not in models:
        raise ValueError(f"Model {model_name} is not supported.")

    model = models[model_name]
    param_grid = param_grids[model_name]
    best_params = grid_search.best_params_
    grid_search = GridSearchCV(model, param_grid, cv=3, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_

    return best_model, best_params
