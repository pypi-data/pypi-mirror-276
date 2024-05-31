import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, Birch, MeanShift, SpectralClustering, AffinityPropagation
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator, ClusterMixin

def scale_data(X):
    """
    Eng: Data scaling.
    Fra: Mise à l'échelle des données.
    Rus: Масштабирование данных.
    Ger: Daten skalieren.

    Parameters:
    X (np.ndarray): An array of data.

    Returns:
    X_scaled (np.ndarray): Scaled data array.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

def kmeans_clustering(df, n_clusters=4, random_state=0):
    """
    Eng: Clustering using K-means.
    Fra: Clustering à l'aide de K-means.
    Rus: Кластеризация с помощью K-means.
    Ger: Clustering mit K-means.

    Parameters:
    df (pd.Data Frame): DataFrame with data.
    n_clusters (int): The number of clusters.
    random_state (int): A parameter for reproducibility.

    Returns:
    df (pd.Data Frame): DataFrame with cluster labels.
    silhouette (float): The value of the silhouette metric.
    """
    X = df.values
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = kmeans.fit_predict(X)
    silhouette = silhouette_score(X, labels)
    df['kmeans_labels'] = labels
    return df, silhouette

def hierarchical_clustering(df, n_clusters=4):
    """
    Eng: Hierarchical clustering.
    Fra: Clustering hiérarchique.
    Rus: Иерархическая кластеризация.
    Ger: Hierarchisches Clustering.

    Parameters:
    df (pd.Data Frame): DataFrame with data.
    n_clusters (int): The number of clusters.

    Returns:
    df (pd.Data Frame): DataFrame with cluster labels.
    silhouette (float): The value of the silhouette metric.
    """
    X = df.values
    hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
    labels = hierarchical.fit_predict(X)
    silhouette = silhouette_score(X, labels)
    df['hierarchical_labels'] = labels
    return df, silhouette

def dbscan_clustering(df, eps=0.3, min_samples=10):
    """
    Eng: Clustering using DBSCAN.
    Fra: Clustering à l'aide de DBSCAN.
    Rus: Кластеризация с помощью DBSCAN.
    Ger: Clustering mit DBSCAN.

    Parameters:
    df (pd.Data Frame): DataFrame with data.
    eps (float): The maximum distance between two samples to combine them into one cluster.
    min_samples (int): The minimum number of samples in the cluster.

    Returns:
    df (pd.Data Frame): DataFrame with cluster labels.
    silhouette (float): The value of the silhouette metric.
    """
    X = df.values
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X)
    silhouette = silhouette_score(X, labels)
    df['dbscan_labels'] = labels
    return df, silhouette

def birch_clustering(df, n_clusters=4):
    """
    Eng: Clustering using BIRCH.
    Fra: Clustering à l'aide de BIRCH.
    Rus: Кластеризация с помощью BIRCH.
    Ger: Clustering mit BIRCH.

    Parameters:
    df (pd.Data Frame): DataFrame with data.
    n_clusters (int): The number of clusters.

    Returns:
    df (pd.Data Frame): DataFrame with cluster labels.
    silhouette (float): The value of the silhouette metric.
    """
    X = df.values
    birch = Birch(n_clusters=n_clusters)
    labels = birch.fit_predict(X)
    silhouette = silhouette_score(X, labels)
    df['birch_labels'] = labels
    return df, silhouette

def mean_shift_clustering(df):
    """
    Eng: Clustering using Mean Shift.
    Fra: Clustering à l'aide de Mean Shift.
    Rus: Кластеризация с помощью Mean Shift.
    Ger: Clustering mit Mean Shift.

    Parameters:
    df (pd.Data Frame): DataFrame with data.

    Returns:
    df (pd.Data Frame): DataFrame with cluster labels.
    silhouette (float): The value of the silhouette metric.
    """
    X = df.values
    mean_shift = MeanShift()
    labels = mean_shift.fit_predict(X)
    silhouette = silhouette_score(X, labels)
    df['mean_shift_labels'] = labels
    return df, silhouette

def spectral_clustering(df, n_clusters=4, random_state=0):
    """
    Eng: Clustering using Spectral Clustering.
    Fra: Clustering à l'aide de Spectral Clustering.
    Rus: Кластеризация с помощью Spectral Clustering.
    Ger: Clustering mit Spectral Clustering.

    Parameters:
    df (pd.Data Frame): DataFrame with data.
    n_clusters (int): The number of clusters.
    random_state (int): A parameter for reproducibility.

    Returns:
    df (pd.Data Frame): DataFrame with cluster labels.
    silhouette (float): The value of the silhouette metric.
    """
    X = df.values
    spectral = SpectralClustering(n_clusters=n_clusters, random_state=random_state)
    labels = spectral.fit_predict(X)
    silhouette = silhouette_score(X, labels)
    df['spectral_labels'] = labels
    return df, silhouette

def affinity_propagation_clustering(df):
    """
    Eng: Clustering using Affinity Propagation.
    Fra: Clustering à l'aide de Affinity Propagation.
    Rus: Кластеризация с помощью Affinity Propagation.
    Ger: Clustering mit Affinity Propagation.

    Parameters:
    df (pd.Data Frame): DataFrame with data.

    Returns:
    df (pd.Data Frame): DataFrame with cluster labels.
    silhouette (float): The value of the silhouette metric.
    """
    X = df.values
    affinity = AffinityPropagation()
    labels = affinity.fit_predict(X)
    silhouette = silhouette_score(X, labels)
    df['affinity_propagation_labels'] = labels
    return df, silhouette

def calculate_metrics(X, labels):
    """
    Eng: Calculation of clustering metrics.
    Fra: Calcul des métriques de clustering.
    Rus: Расчет метрик кластеризации.
    Ger: Berechnung von Clustering-Metriken.

    Parameters:
    X (np.ndarray): An array of data.
    labels (np.ndarray): An array of cluster labels.

    Returns:
    metrics (dict): A dictionary with clustering metrics.
    """
    silhouette = silhouette_score(X, labels)
    calinski_harabasz = calinski_harabasz_score(X, labels)
    davies_bouldin = davies_bouldin_score(X, labels)
    
    metrics = {
        'silhouette': silhouette,
        'calinski_harabasz': calinski_harabasz,
        'davies_bouldin': davies_bouldin
    }
    return metrics

def plot_clusters(df, label_col, title):
    """
    Eng: Clustering visualization.
    Fra: Visualisation des clusters.
    Rus: Визуализация кластеров.
    Ger: Visualisierung der Cluster.

    Parameters:
    df (pd.Data Frame): DataFrame with data.
    label_col (str): The name of the column with cluster labels.
    title (str): The title of the graph.
    """
    if df.shape[1] < 2:
        raise ValueError("DataFrame должен содержать как минимум два столбца для визуализации.")
        
    plt.scatter(df.iloc[:, 0], df.iloc[:, 1], c=df[label_col], s=50, cmap='viridis')
    plt.title(title)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()

class ClusteringModel(BaseEstimator, ClusterMixin):
    def __init__(self, model_name='kmeans', **params):
        self.model_name = model_name
        self.params = params
        self.model = self._create_model()

    def _create_model(self):
        if self.model_name == 'kmeans':
            return KMeans(**self.params)
        elif self.model_name == 'hierarchical':
            return AgglomerativeClustering(**self.params)
        elif self.model_name == 'dbscan':
            return DBSCAN(**self.params)
        elif self.model_name == 'birch':
            return Birch(**self.params)
        elif self.model_name == 'mean_shift':
            return MeanShift(**self.params)
        elif self.model_name == 'spectral':
            return SpectralClustering(**self.params)
        elif self.model_name == 'affinity_propagation':
            return AffinityPropagation(**self.params)
        else:
            raise ValueError(f"Unknown model_name: {self.model_name}")

    def fit(self, X, y=None):
        self.model.fit(X)
        return self

    def fit_predict(self, X, y=None):
        return self.model.fit_predict(X)

def optimize_clustering(X, model_name, param_grid, cv=3, scoring='silhouette'):
    """
    Eng: Hyperparameter optimization for clustering using GridSearchCV.
    Fra: Optimisation des hyperparamètres pour le clustering en utilisant GridSearchCV.
    Rus: Оптимизация гиперпараметров для кластеризации с использованием GridSearchCV.
    Ger: Hyperparameteroptimierung für Clustering mit GridSearchCV.

    Parameters:
    X (np.ndarray): An array of data.
    model_name (str): Name of the clustering model ('kmeans', 'hierarchical', 'dbscan', 'birch', 'mean_shift', 'spectral', 'affinity_propagation').
    param_grid (dict): A dictionary with parameters for configuring hyperparameters.
    cv (int): The number of folds for cross validation.
    scoring (str): Metric for evaluation ('silhouette', 'calinski_harabasz', 'davies_bouldin').

    Returns:
    best_model (Clustering Model): The best model after configuring hyperparameters.
    """
    model = ClusteringModel(model_name=model_name)
    grid_search = GridSearchCV(model, param_grid, cv=cv, scoring=scoring, n_jobs=-1)
    grid_search.fit(X)
    
    best_model = grid_search.best_estimator_
    return best_model