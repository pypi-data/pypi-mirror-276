import psycopg2
from pymongo import MongoClient
import mysql.connector
import sqlite3
import pandas as pd

# PostgreSQL functions
def add_postgresql_record(conn, table, data):
    """
    Eng: Adds a record to the PostgreSQL table.
    Fra: Ajoute un enregistrement à la table PostgreSQL.
    Rus: Добавляет запись в таблицу PostgreSQL.
    Ger: Fügt einen Datensatz zur PostgreSQL-Tabelle hinzu.
    """
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    with conn.cursor() as cursor:
        cursor.execute(sql, list(data.values()))
    conn.commit()

def delete_postgresql_record(conn, table, condition):
    """
    Eng: Deletes a record from the PostgreSQL table.
    Fra: Supprime un enregistrement de la table PostgreSQL.
    Rus: Удаляет запись из таблицы PostgreSQL.
    Ger: Löscht einen Datensatz aus der PostgreSQL-Tabelle.
    """
    sql = f"DELETE FROM {table} WHERE {condition}"
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()

def update_postgresql_record(conn, table, data, condition):
    """
    Eng: Updates a record in the PostgreSQL table.
    Fra: Met à jour un enregistrement dans la table PostgreSQL.
    Rus: Обновляет запись в таблице PostgreSQL.
    Ger: Aktualisiert einen Datensatz in der PostgreSQL-Tabelle.
    """
    set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
    sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
    with conn.cursor() as cursor:
        cursor.execute(sql, list(data.values()))
    conn.commit()

def clean_postgresql_data(conn, table, method, column=None, value=None, lower_bound=None, upper_bound=None):
    """
    Eng: Cleans data in the PostgreSQL table by the specified method.
    Fra: Nettoie les données dans la table PostgreSQL en utilisant la méthode spécifiée.
    Rus: Очищает данные в таблице PostgreSQL с использованием указанного метода.
    Ger: Bereinigt Daten in der PostgreSQL-Tabelle mit der angegebenen Methode.
    """
    cursor = conn.cursor()
    cursor.execute("ROLLBACK")
    conn.commit()
    if method == 'dropna':
        sql = f"DELETE FROM {table} WHERE {column} IS NULL"
    elif method == 'fillna':
        sql = f"UPDATE {table} SET {column} = %s WHERE {column} IS NULL" % value
    elif method == 'drop_duplicates':
        sql = f"DELETE FROM {table} WHERE ctid NOT IN (SELECT min(ctid) FROM {table} GROUP BY {column})"
    elif method == 'remove_outliers':
        sql = f"DELETE FROM {table} WHERE {column} < {lower_bound} OR {column} > {upper_bound}"
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()

def fetch_postgresql_to_dataframe(table, conn):
    """
    Eng: Fetches data from PostgreSQL table to a DataFrame.
    Fra: Récupère des données de la table PostgreSQL dans un DataFrame.
    Rus: Извлекает данные из таблицы PostgreSQL в DataFrame.
    Ger: Holt Daten aus der PostgreSQL-Tabelle in ein DataFrame.
    """
    cursor = conn.cursor()
    cursor.execute("ROLLBACK")
    conn.commit()
    cursor.execute(f"SELECT * FROM {table}")

    results = cursor.fetchall()
    df = pd.DataFrame(results)
    return df

# MongoDB functions
def add_mongodb_record(db, collection, data):
    """
    Eng: Adds a record to the MongoDB collection.
    Fra: Ajoute un enregistrement à la collection MongoDB.
    Rus: Добавляет запись в коллекцию MongoDB.
    Ger: Fügt einen Datensatz zur MongoDB-Sammlung hinzu.
    """
    db[collection].insert_one(data)

def delete_mongodb_record(db, collection, condition):
    """
    Eng: Deletes a record from the MongoDB collection.
    Fra: Supprime un enregistrement de la collection MongoDB.
    Rus: Удаляет запись из коллекции MongoDB.
    Ger: Löscht einen Datensatz aus der MongoDB-Sammlung.
    """
    db[collection].delete_one(condition)

def update_mongodb_record(db, collection, condition, data):
    """
    Eng: Updates a record in the MongoDB collection.
    Fra: Met à jour un enregistrement dans la collection MongoDB.
    Rus: Обновляет запись в коллекции MongoDB.
    Ger: Aktualisiert einen Datensatz in der MongoDB-Sammlung.
    """
    db[collection].update_one(condition, {'$set': data})

def fetch_mongodb_to_dataframe(db, collection, query):
    """
    Eng: Fetches data from MongoDB collection to a DataFrame.
    Fra: Récupère des données de la collection MongoDB dans un DataFrame.
    Rus: Извлекает данные из коллекции MongoDB в DataFrame.
    Ger: Holt Daten aus der MongoDB-Sammlung in ein DataFrame.
    """
    cursor = db[collection].find(query)
    df = pd.DataFrame(list(cursor))
    return df

# MySQL functions
def add_mysql_record(conn, table, data):
    """
    Eng: Adds a record to the MySQL table.
    Fra: Ajoute un enregistrement à la table MySQL.
    Rus: Добавляет запись в таблицу MySQL.
    Ger: Fügt einen Datensatz zur MySQL-Tabelle hinzu.
    """
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    with conn.cursor() as cursor:
        cursor.execute(sql, list(data.values()))
    conn.commit()

def delete_mysql_record(conn, table, condition):
    """
    Eng: Deletes a record from the MySQL table.
    Fra: Supprime un enregistrement de la table MySQL.
    Rus: Удаляет запись из таблицы MySQL.
    Ger: Löscht einen Datensatz aus der MySQL-Tabelle.
    """
    sql = f"DELETE FROM {table} WHERE {condition}"
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()

def update_mysql_record(conn, table, data, condition):
    """
    Eng: Updates a record in the MySQL table.
    Fra: Met à jour un enregistrement dans la table MySQL.
    Rus: Обновляет запись в таблице MySQL.
    Ger: Aktualisiert einen Datensatz in der MySQL-Tabelle.
    """
    set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
    sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
    with conn.cursor() as cursor:
        cursor.execute(sql, list(data.values()))
    conn.commit()

def clean_mysql_data(conn, table, method, column=None, value=None, lower_bound=None, upper_bound=None):
    """
    Eng: Cleans data in the MySQL table by the specified method.
    Fra: Nettoie les données dans la table MySQL en utilisant la méthode spécifiée.
    Rus: Очищает данные в таблице MySQL с использованием указанного метода.
    Ger: Bereinigt Daten in der MySQL-Tabelle mit der angegebenen Methode.
    """
    if method == 'dropna':
        sql = f"DELETE FROM {table} WHERE {column} IS NULL"
    elif method == 'fillna':
        sql = f"UPDATE {table} SET {column} = %s WHERE {column} IS NULL" % value
    elif method == 'drop_duplicates':
        sql = f"DELETE FROM {table} WHERE id NOT IN (SELECT min(id) FROM {table} GROUP BY {column})"
    elif method == 'remove_outliers':
        sql = f"DELETE FROM {table} WHERE {column} < {lower_bound} OR {column} > {upper_bound}"
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()

def fetch_mysql_to_dataframe(conn, query):
    """
    Eng: Fetches data from MySQL table to a DataFrame.
    Fra: Récupère des données de la table MySQL dans un DataFrame.
    Rus: Извлекает данные из таблицы MySQL в DataFrame.
    Ger: Holt Daten aus der MySQL-Tabelle in ein DataFrame.
    """
    df = pd.read_sql_query(query, conn)
    return df

# SQLite functions
def add_sqlite_record(conn, table, data):
    """
    Eng: Adds a record to the SQLite table.
    Fra: Ajoute un enregistrement à la table SQLite.
    Rus: Добавляет запись в таблицу SQLite.
    Ger: Fügt einen Datensatz zur SQLite-Tabelle hinzu.
    """
    placeholders = ', '.join(['?'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    conn.execute(sql, list(data.values()))
    conn.commit()

def delete_sqlite_record(conn, table, condition):
    """
    Eng: Deletes a record from the SQLite table.
    Fra: Supprime un enregistrement de la table SQLite.
    Rus: Удаляет запись из таблицы SQLite.
    Ger: Löscht einen Datensatz aus der SQLite-Tabelle.
    """
    sql = f"DELETE FROM {table} WHERE {condition}"
    conn.execute(sql)
    conn.commit()

def update_sqlite_record(conn, table, data, condition):
    """
    Eng: Updates a record in the SQLite table.
    Fra: Met à jour un enregistrement dans la table SQLite.
    Rus: Обновляет запись в таблице SQLite.
    Ger: Aktualisiert einen Datensatz in der SQLite-Tabelle.
    """
    set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
    sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
    conn.execute(sql, list(data.values()))
    conn.commit()

def clean_sqlite_data(conn, table, method, column=None, value=None, lower_bound=None, upper_bound=None):
    """
    Eng: Cleans data in the SQLite table by the specified method.
    Fra: Nettoie les données dans la table SQLite en utilisant la méthode spécifiée.
    Rus: Очищает данные в таблице SQLite с использованием указанного метода.
    Ger: Bereinigt Daten in der SQLite-Tabelle mit der angegebenen Methode.
    """
    if method == 'dropna':
        sql = f"DELETE FROM {table} WHERE {column} IS NULL"
    elif method == 'fillna':
        sql = f"UPDATE {table} SET {column} = ? WHERE {column} IS NULL" % value
    elif method == 'drop_duplicates':
        sql = f"DELETE FROM {table} WHERE rowid NOT IN (SELECT min(rowid) FROM {table} GROUP BY {column})"
    elif method == 'remove_outliers':
        sql = f"DELETE FROM {table} WHERE {column} < {lower_bound} OR {column} > {upper_bound}"
    conn.execute(sql)
    conn.commit()

def fetch_sqlite_to_dataframe(conn, query):
    """
    Eng: Fetches data from SQLite table to a DataFrame.
    Fra: Récupère des données de la table SQLite dans un DataFrame.
    Rus: Извлекает данные из таблицы SQLite в DataFrame.
    Ger: Holt Daten aus der SQLite-Tabelle in ein DataFrame.
    """
    df = pd.read_sql_query(query, conn)
    return df

# Microsoft SQL Server functions
def add_mssql_record(conn, table, data):
    """
    Eng: Adds a record to the MSSQL table.
    Fra: Ajoute un enregistrement à la table MSSQL.
    Rus: Добавляет запись в таблицу MSSQL.
    Ger: Fügt einen Datensatz zur MSSQL-Tabelle hinzu.
    """
    placeholders = ', '.join(['?'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    with conn.cursor() as cursor:
        cursor.execute(sql, list(data.values()))
    conn.commit()

def delete_mssql_record(conn, table, condition):
    """
    Eng: Deletes a record from the MSSQL table.
    Fra: Supprime un enregistrement de la table MSSQL.
    Rus: Удаляет запись из таблицы MSSQL.
    Ger: Löscht einen Datensatz aus der MSSQL-Tabelle.
    """
    sql = f"DELETE FROM {table} WHERE {condition}"
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()

def update_mssql_record(conn, table, data, condition):
    """
    Eng: Updates a record in the MSSQL table.
    Fra: Met à jour un enregistrement dans la table MSSQL.
    Rus: Обновляет запись в таблице MSSQL.
    Ger: Aktualisiert einen Datensatz in der MSSQL-Tabelle.
    """
    set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
    sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
    with conn.cursor() as cursor:
        cursor.execute(sql, list(data.values()))
    conn.commit()

def clean_mssql_data(conn, table, method, column=None, value=None, lower_bound=None, upper_bound=None):
    """
    Eng: Cleans data in the MSSQL table by the specified method.
    Fra: Nettoie les données dans la table MSSQL en utilisant la méthode spécifiée.
    Rus: Очищает данные в таблице MSSQL с использованием указанного метода.
    Ger: Bereinigt Daten in der MSSQL-Tabelle mit der angegebenen Methode.
    """
    if method == 'dropna':
        sql = f"DELETE FROM {table} WHERE {column} IS NULL"
    elif method == 'fillna':
        sql = f"UPDATE {table} SET {column} = ? WHERE {column} IS NULL" % value
    elif method == 'drop_duplicates':
        sql = f"DELETE FROM {table} WHERE id NOT IN (SELECT min(id) FROM {table} GROUP BY {column})"
    elif method == 'remove_outliers':
        sql = f"DELETE FROM {table} WHERE {column} < {lower_bound} OR {column} > {upper_bound}"
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()

def fetch_mssql_to_dataframe(conn, query):
    """
    Eng: Fetches data from MSSQL table to a DataFrame.
    Fra: Récupère des données de la table MSSQL dans un DataFrame.
    Rus: Извлекает данные из таблицы MSSQL в DataFrame.
    Ger: Holt Daten aus der MSSQL-Tabelle in ein DataFrame.
    """
    df = pd.read_sql_query(query, conn)
    return df

# Functions for loading data into DataFrames
def load_csv_to_dataframe(filepath):
    """
    Eng: Loads a CSV file into a DataFrame.
    Fra: Charge un fichier CSV dans un DataFrame.
    Rus: Загружает CSV файл в DataFrame.
    Ger: Lädt eine CSV-Datei in ein DataFrame.
    """
    return pd.read_csv(filepath)

def load_json_to_dataframe(filepath):
    """
    Eng: Loads a JSON file into a DataFrame.
    Fra: Charge un fichier JSON dans un DataFrame.
    Rus: Загружает JSON файл в DataFrame.
    Ger: Lädt eine JSON-Datei in ein DataFrame.
    """
    return pd.read_json(filepath)

# Functions for inserting DataFrame data into databases
def dataframe_to_postgresql(conn, table, df):
    """
    Eng: Inserts a DataFrame into the PostgreSQL table.
    Fra: Insère un DataFrame dans la table PostgreSQL.
    Rus: Вставляет DataFrame в таблицу PostgreSQL.
    Ger: Fügt ein DataFrame in die PostgreSQL-Tabelle ein.
    """
    cursor = conn.cursor()
    cursor.execute("ROLLBACK")
    tuples = [tuple(x) for x in df.to_numpy()]
    
    # Имена столбцов обрамляем в двойные кавычки для PostgreSQL
    cols = ','.join([f'"{col}"' for col in df.columns])
    
    # SQL placeholders
    placeholders = ','.join(['%s'] * len(df.columns))
    
    # Построение SQL-запроса с использованием безопасного синтаксиса
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    with conn.cursor() as cursor:
        cursor.executemany(sql, tuples)
    conn.commit()


def dataframe_to_mongodb(db, collection, df):
    """
    Eng: Inserts a DataFrame into the MongoDB collection.
    Fra: Insère un DataFrame dans la collection MongoDB.
    Rus: Вставляет DataFrame в коллекцию MongoDB.
    Ger: Fügt ein DataFrame in die MongoDB-Sammlung ein.
    """
    db[collection].insert_many(df.to_dict('records'))

def dataframe_to_mysql(conn, table, df):
    """
    Eng: Inserts a DataFrame into the MySQL table.
    Fra: Insère un DataFrame dans la table MySQL.
    Rus: Вставляет DataFrame в таблицу MySQL.
    Ger: Fügt ein DataFrame in die MySQL-Tabelle ein.
    """
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ', '.join(list(df.columns))
    placeholders = ', '.join(['%s'] * len(df.columns))
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    with conn.cursor() as cursor:
        cursor.executemany(sql, tuples)
    conn.commit()

def dataframe_to_sqlite(conn, table, df):
    """
    Eng: Inserts a DataFrame into the SQLite table.
    Fra: Insère un DataFrame dans la table SQLite.
    Rus: Вставляет DataFrame в таблицу SQLite.
    Ger: Fügt ein DataFrame in die SQLite-Tabelle ein.
    """
    df.to_sql(table, conn, if_exists='append', index=False)

def dataframe_to_mssql(conn, table, df):
    """
    Eng: Inserts a DataFrame into the MSSQL table.
    Fra: Insère un DataFrame dans la table MSSQL.
    Rus: Вставляет DataFrame в таблицу MSSQL.
    Ger: Fügt ein DataFrame in die MSSQL-Tabelle ein.
    """
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ', '.join(list(df.columns))
    placeholders = ', '.join(['?'] * len(df.columns))
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    with conn.cursor() as cursor:
        cursor.executemany(sql, tuples)
    conn.commit()