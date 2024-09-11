import streamlit as st
import pandas as pd
from computer_db_helper import insert_computer_in_bulk, insert_computer_manually

st.title("Agregar información de los equipos de cómputo")

def extract_computers_from_excel(excel_file1, excel_file2):
    
    try:
        df1 = pd.read_excel(excel_file1)
        df2 = pd.read_excel(excel_file2)
    except Exception as e:
        st.write(f"Error en la lectura del archivo en excel: {e}")
        return []

    
    df1 = df1[['serial', 'marca', 'modelo']]
    df2 = df2[['procesador', 'memoria_ram', 'almacenamiento', 'tipo']]

    
    concat_df = pd.concat([df1, df2], axis=1)

    
    insert_computer_in_bulk(concat_df, table_name='computer')

    st.write(concat_df)

    st.success("¡La información se ha registrado exitosamente!")
    

def form_manual():
    
    st.subheader("Agregar información de equipo de cómputo")

    # Crear campos de entrada en el formulario
    serial = st.text_input("Serial")
    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo")
    procesador = st.text_input("Procesador")
    memoria_ram = st.text_input("Memoria RAM")
    almacenamiento = st.text_input("Almacenamiento")
    tipo = st.text_input("Tipo")

    
    if st.button("Agregar datos"):
        if serial and marca and modelo and procesador and memoria_ram and almacenamiento and tipo:
            # Llamar la función para insertar en la base de datos
            insert_computer_manually(serial, marca, modelo, procesador, memoria_ram, almacenamiento, tipo)
            st.success("¡La información se ha registrado exitosamente!")
        else:
            st.error("Por favor complete todos los campos.")


form_manual()


st.subheader("Subir lista de información de equipos de cómputo")
uploaded_file1 = st.file_uploader("Por favor agregue el archivo que contiene los datos de los equipos:", type=["xls", "xlsx"])
uploaded_file2 = st.file_uploader("Por favor agregue el archivo con las especificaciones de los equipos:", type=["xls", "xlsx"])


if st.button("Agregar datos de archivos"):
    if uploaded_file1 is not None and uploaded_file2 is not None:
        extract_computers_from_excel(uploaded_file1, uploaded_file2)
    else:
        st.error("Por favor cargue los dos archivos solicitados")

