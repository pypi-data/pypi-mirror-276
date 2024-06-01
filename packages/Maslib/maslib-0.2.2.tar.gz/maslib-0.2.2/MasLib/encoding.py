from sklearn import preprocessing
import pandas as pd
import numpy as np
import pandas as pd

def number_encode_features(init_df: pd.DataFrame) -> (pd.DataFrame, dict):
    """
    Eng: Function for encoding categorical features into numerical ones.
    Fra: Fonction pour encoder les caractéristiques catégorielles en numériques.
    Rus: Функция для кодирования категориальных признаков в числовые.
    Ger: Funktion zum Codieren kategorischer Merkmale in numerische.

    Parameters:
    init_df (pd.Data Frame): The original DataFrame.

    Returns:
    result (pd.Data Frame): A DataFrame with encoded attributes.
    encoders (dict): A dictionary with a LabelEncoder for each categorical feature.
    """
    result = init_df.copy()
    encoders = {}
    for column in result.columns:
        if result.dtypes[column] == object:
            encoders[column] = preprocessing.LabelEncoder()
            result[column] = encoders[column].fit_transform(result[column])
    return result, encoders

def process_column_and_merge(df_main, column_name):
    """
    Eng: Function for processing the specified column of a DataFrame, extracting values, and merging with an additional DataFrame.
    Fra: Fonction pour le traitement de la colonne spécifiée d'un DataFrame, l'extraction des valeurs et la fusion avec un DataFrame supplémentaire.
    Rus: Функция для обработки указанного столбца DataFrame, извлечения значений и объединения с дополнительным DataFrame.
    Ger: Funktion zur Verarbeitung der angegebenen Spalte eines DataFrame, Extrahierung von Werten und Zusammenführung mit einem zusätzlichen DataFrame.

    Parameters:
    df_main (pd.DataFrame): The main DataFrame.
    column_name (str): The name of the column to be processed.

    Returns:
    pd.Data Frame: The main DataFrame with the processed and merged column.

    """
    
    danger = []
    except_value = [np.nan, np.nan]
    
    for row in range(df_main.shape[0]):
        try:
            danger.append(list(df_main[column_name])[row].values())
        except:
            danger.append(except_value)
    
    data_points = pd.DataFrame(columns=list(df_main[column_name])[0].keys(), data=danger)
    
    df_main = pd.concat([df_main, data_points], axis=1)
    
    return df_main

def json_to_dataframe(json_path,name,name1,name3):
    """
    Eng: Function for converting data from JSON to DataFrame and creating a dictionary.
    Fra: Fonction pour convertir les données de JSON en DataFrame et créer un dictionnaire.
    Rus: Функция для преобразования данных из JSON в DataFrame и создания словаря.
    Ger: Funktion zum Konvertieren von Daten aus JSON in DataFrame und Erstellen eines Wörterbuchs.

    Parameters:
    json_path (str): The path to the JSON file.
    name (str): The name of the key for uploading data to the Data Frame.
    name 1 (str): The name of the column with the company name.
    name 3 (str): The name of the column with the nomination.

    Returns:
    df_json (pd.Data Frame): Data Frame with data from JSON.
    dict1 (dict): A dictionary where the keys are companies and the values are nominations.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        target = json.load(f)
    df_json = pd.DataFrame(target[name])
    dict1 = {}
    for company, nomination in zip(df_json[name2], df_json[name3]):
        dict1[company] = nomination
    return df_json, dict1



