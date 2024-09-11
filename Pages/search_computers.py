import streamlit as st
import pandas as pd
from computer_db_helper import get_computer_info, get_all_brands

st.title("Consultar información de los equipos de cómputo por marca")

# Obtener la lista de todas las marcas desde la base de datos
brands = get_all_brands()

# Si hay marcas disponibles, mostrar el dropdown
if brands:
    st.header("Buscar equipos de cómputo por marca:")
    marca_seleccionada = st.selectbox("Seleccione una marca", options=brands)
    
    # Botón para realizar la consulta
    if st.button("Consultar"):
        if marca_seleccionada:
            # Realizar la consulta a la base de datos con la marca seleccionada
            results = get_computer_info(marca=marca_seleccionada)

            if results:
                st.write(f"Found {len(results)} computer(s) with the brand '{marca_seleccionada}':")
                # Mostrar los resultados en una tabla
                df = pd.DataFrame(results, columns=['Serial', 'Marca', 'Modelo', 'Procesador', 'Memoria RAM', 'Almacenamiento', 'Tipo'])
                st.dataframe(df)
            else:
                st.write(f"Equipos no encontrados '{marca_seleccionada}'.")
        else:
            st.write("Por favor seleccione una marca.")
else:
    st.write("No hay marcas disponibles en la base de datos.")