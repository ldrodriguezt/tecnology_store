import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def clean_dataframe(df):
    """Limpia el DataFrame de valores NaN en nombres de columnas y datos."""
    df.columns = df.columns.fillna('')
    df = df.fillna('')
    return df

def insert_computer_in_bulk(merged_df, table_name='computer'):
    connection = None
    cursor = None

    try:
        
        if not table_name.isidentifier():
            raise ValueError("Invalid table name.")

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            #port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Limpia el DataFrame
            merged_df = clean_dataframe(merged_df)

            # Verifica que el DataFrame tenga las columnas necesarias
            expected_columns = {'serial', 'marca', 'modelo', 'procesador', 'memoria_ram', 'almacenamiento', 'tipo'}
            if not expected_columns.issubset(set(merged_df.columns)):
                raise ValueError("DataFrame is missing one or more expected columns.")

            # Prepare the insert query
            insert_query = f"""
            INSERT INTO {table_name} (serial, marca, modelo, procesador, memoria_ram, almacenamiento, tipo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            # Convert DataFrame to list of tuples
            computer_data = merged_df.to_records(index=False).tolist()

            # Execute the insert query in bulk
            cursor.executemany(insert_query, computer_data)
            
            # Commit the transaction
            connection.commit()

            print(f"{cursor.rowcount} rows inserted successfully.")

    except Error as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()
    except ValueError as ve:
        print(f"ValueError: {ve}")

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

