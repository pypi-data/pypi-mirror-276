import joblib
import pandas as pd
import json
import xml.etree.ElementTree as ET
import yaml
import fastavro
import pyorc
import pickle
import pdfplumber
from io import BytesIO


import pandas as pd
import json
import xml.etree.ElementTree as ET
import yaml
import fastavro
import pyorc
import pickle
import pdfplumber
import pyreadstat
import sas7bdat
import cbor2
from sqlalchemy import create_engine
from io import BytesIO

def read_file(file_path, file_type):
    """
    Eng: Function to read different types of data files into a DataFrame.
    Fra: Fonction pour lire différents types de fichiers de données dans un DataFrame.
    Rus: Функция для чтения различных типов файлов данных в DataFrame.
    Ger: Funktion zum Lesen verschiedener Arten von Datendateien in ein DataFrame.

    Parameters:
    file_path (str): The path to the file to be read.
    file_type (str): The type of the file ('csv', 'json', 'xml', 'tskv', 'yaml', 'parquet', 'excel', 'hdf5', 'html', 'feather', 'avro', 'orc', 'stata', 'pickle', 'pdf', 'sql', 'spss', 'sas', 'cbor').
    
    Returns:
    pd.DataFrame: DataFrame containing the data from the file.
    """
    if file_type == 'csv':
        return pd.read_csv(file_path)
    elif file_type == 'json':
        return pd.read_json(file_path)
    elif file_type == 'xml':
        return read_xml(file_path)
    elif file_type == 'tskv':
        return read_tskv(file_path)
    elif file_type == 'yaml':
        return read_yaml(file_path)
    elif file_type == 'parquet':
        return pd.read_parquet(file_path)
    elif file_type == 'excel':
        return pd.read_excel(file_path)
    elif file_type == 'hdf5':
        return pd.read_hdf(file_path)
    elif file_type == 'html':
        return pd.read_html(file_path)[0]
    elif file_type == 'feather':
        return pd.read_feather(file_path)
    elif file_type == 'avro':
        return read_avro(file_path)
    elif file_type == 'orc':
        return read_orc(file_path)
    elif file_type == 'stata':
        return pd.read_stata(file_path)
    elif file_type == 'pickle':
        return read_pickle(file_path)
    elif file_type == 'pdf':
        return read_pdf(file_path)
    elif file_type == 'sql':
        return read_sql(file_path)
    elif file_type == 'spss':
        return read_spss(file_path)
    elif file_type == 'sas':
        return read_sas(file_path)
    elif file_type == 'cbor':
        return read_cbor(file_path)
    else:
        raise ValueError("Unsupported file type")

def read_tskv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        pairs = line.strip().split('\t')
        record = {}
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                record[key] = value
        data.append(record)
    
    return pd.DataFrame(data)

def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    data = []
    for child in root:
        record = {}
        for subchild in child:
            record[subchild.tag] = subchild.text
        data.append(record)
    
    return pd.DataFrame(data)

def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    
    return pd.DataFrame(data)

def read_avro(file_path):
    with open(file_path, 'rb') as file:
        reader = fastavro.reader(file)
        records = [record for record in reader]
    
    return pd.DataFrame(records)

def read_orc(file_path):
    with open(file_path, 'rb') as file:
        reader = pyorc.Reader(file)
        columns = reader.schema.fields
        data = {col: [] for col in columns}
        
        for row in reader:
            for col, value in zip(columns, row):
                data[col].append(value)
    
    return pd.DataFrame(data)

def read_pickle(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    
    return pd.DataFrame(data)

def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    
    text = '\n'.join(pages)
    lines = text.split('\n')
    data = [line.split() for line in lines if line]
    
    return pd.DataFrame(data)

def read_sql(file_path):
    engine = create_engine(f'sqlite:///{file_path}')
    query = "SELECT * FROM table_name" 
    return pd.read_sql_query(query, engine)

def read_spss(file_path):
    df, meta = pyreadstat.read_sav(file_path)
    return df

def read_sas(file_path):
    with sas7bdat.SAS7BDAT(file_path) as file:
        df = file.to_data_frame()
    return df

def read_cbor(file_path):
    with open(file_path, 'rb') as file:
        data = cbor2.load(file)
    return pd.DataFrame(data)

