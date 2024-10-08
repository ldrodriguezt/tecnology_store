import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


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

def insert_computer_manually(serial, marca, modelo, procesador, memoria_ram, almacenamiento, tipo, table_name='computer'):
    connection = None
    cursor = None

    try:
        if not table_name.isidentifier():
            raise ValueError("Invalid table name.")

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Prepare the insert query for a single record
            insert_query = f"""
            INSERT INTO {table_name} (serial, marca, modelo, procesador, memoria_ram, almacenamiento, tipo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            # Execute the insert query with the provided data
            cursor.execute(insert_query, (serial, marca, modelo, procesador, memoria_ram, almacenamiento, tipo))
            
            # Commit the transaction
            connection.commit()

            print(f"1 row inserted successfully.")

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


def get_computer_info(serial=None, marca=None, modelo=None, table_name='computer'):
    connection = None
    cursor = None
    results = []

    try:
        if not table_name.isidentifier():
            raise ValueError("Invalid table name.")

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Crear una consulta dinámica dependiendo de los criterios proporcionados
            query = f"SELECT serial, marca, modelo, procesador, memoria_ram, almacenamiento, tipo FROM {table_name} WHERE 1=1"
            params = []

            if serial:
                query += " AND serial = %s"
                params.append(serial)
            if marca:
                query += " AND marca = %s"
                params.append(marca)
            if modelo:
                query += " AND modelo = %s"
                params.append(modelo)

            cursor.execute(query, tuple(params))
            results = cursor.fetchall()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

    return results


# Función para obtener todas las marcas disponibles en la base de datos
def get_all_brands(table_name='computer'):
    connection = None
    cursor = None
    brands = []

    try:
        if not table_name.isidentifier():
            raise ValueError("Invalid table name.")

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Consulta para obtener todas las marcas únicas de la tabla
            query = f"SELECT DISTINCT marca FROM {table_name} ORDER BY marca"
            cursor.execute(query)

            # Obtener todas las marcas y guardarlas en una lista
            brands = [row[0] for row in cursor.fetchall()]

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

    return brands