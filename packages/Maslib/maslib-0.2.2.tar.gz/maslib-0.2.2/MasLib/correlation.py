import pandas as pd
import matplotlib.pyplot as plt
from phik import resources, report
from phik.report import plot_correlation_matrix

def compute_phik_matrix(encoded_data: pd.DataFrame) -> pd.DataFrame:
    """
    Eng: Computes the PhiK matrix for the given DataFrame.
    Fra: Calcule la matrice PhiK pour le DataFrame donné.
    Rus: Вычисляет матрицу PhiK для заданного DataFrame.
    Ger: Berechnet die PhiK-Matrix für das angegebene DataFrame.

    Parameters:
    encoded_data (pd.Data Frame): Data Frame with encoded attributes.

    Returns:
    pd.Data Frame: Phi K correlation matrix.
    """
    interval_cols = list(encoded_data.columns)
    phik_overview = encoded_data.phik_matrix(interval_cols=interval_cols)
    return phik_overview

def plot_phik_correlation_matrix(phik_matrix: pd.DataFrame, color_map="Greens", title="Correlation of features", figsize=(20, 10)):
    """
    Eng: Constructs the PhiK correlation matrix.
    Fra: Construit la matrice de corrélation PhiK.
    Rus: Строит матрицу корреляции PhiK.
    Ger: Konstruiert die PhiK-Korrelationsmatrix.

    Parameters:
    peak_matrix (pd.Data Frame): The Phi K correlation matrix.
    color_map (str): A color scheme for building a matrix.
    title (str): The title of the graph.
    figsize (tuple): The size of the graph shape.
    """
    plot_correlation_matrix(phik_matrix.values,
                            x_labels=phik_matrix.columns,
                            y_labels=phik_matrix.index,
                            vmin=0, vmax=1, color_map=color_map,
                            title=title,
                            fontsize_factor=1.5,
                            figsize=figsize)
    plt.tight_layout()
    plt.show()
