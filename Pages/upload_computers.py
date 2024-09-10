import streamlit as st
import pandas as pd
from computer_db_helper import insert_computer_in_bulk

st.title("Upload computers list.")

def extract_computers_from_excel(excel_file1, excel_file2):
    """Extracts computer information from the provided Excel file."""
    try:
        df1 = pd.read_excel(excel_file1)
        df2 = pd.read_excel(excel_file2)
    except Exception as e:
        st.write(f"Error reading the Excel file: {e}")
        return []

    df1 = df1[['serial', 'marca', 'modelo']]
    df2 = df2[['procesador', 'memoria_ram', 'almacenamiento', 'tipo']]

    # Concatenar ambos DataFrames y eliminar duplicados por la primera columna ('serial')
    #merged_df = pd.merge(df1, df2)
    merged_df = pd.concat([df1, df2], axis=1)

    insert_computer_in_bulk(merged_df, table_name='computer')
    
    st.write(merged_df)

# Subir el archivo de Excel
uploaded_file1 = st.file_uploader("Upload first Excel file", type=["xls", "xlsx"])
uploaded_file2 = st.file_uploader("Upload second Excel file", type=["xls", "xlsx"])

# Botón para procesar la carga y mostrar los valores
if st.button("Save computers"):
    if uploaded_file1 is not None and uploaded_file2 is not None:
        extract_computers_from_excel(uploaded_file1, uploaded_file2)
        st.write("computers have been created successfully")
    