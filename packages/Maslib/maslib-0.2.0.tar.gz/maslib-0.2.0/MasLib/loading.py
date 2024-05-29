import joblib

def save_model(model, file_path='best_model.pkl'):
    """
    Eng: Function for saving the model to a file.
    Fra: Fonction pour enregistrer le modèle dans un fichier.
    Rus: Функция для сохранения модели в файл.
    Ger: Funktion zum Speichern des Modells in einer Datei.

    Parameters:
    model: The model that needs to be saved.
    file_path (str): The path to the file where the model will be saved.
    """
    joblib.dump(model, file_path)
    print(f"The model is saved in {file_path}")