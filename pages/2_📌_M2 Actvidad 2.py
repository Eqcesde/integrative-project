import streamlit as st
import pandas as pd
import io
import os

st.set_page_config(page_title="Explorador de Estudiantes", layout="wide")

# Configuración de la página


st.title("Momento 2 - Actividad 2")

st.header("Descripción de la actividad")
st.markdown("""
Esta actividad es una introducción práctica a Python y a las estructuras de datos básicas.
En ella, exploraremos los conceptos fundamentales de Python y aprenderemos a utilizar variables,
tipos de datos, operadores, y las estructuras de datos más utilizadas como listas, tuplas,
diccionarios y conjuntos.
""")

st.header("Objetivos de aprendizaje")

st.markdown("""
- Comprender los tipos de datos básicos en Python
- Aprender a utilizar variables y operadores
- Dominar las estructuras de datos fundamentales
- Aplicar estos conocimientos en ejemplos prácticos
""")

st.header("Solución")

st.title("📊 Explorador de Estudiantes - Colombia")

# Función para cargar los datos de forma robusta
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.dirname(__file__))  # Subimos a la raíz del proyecto
    file_path = os.path.join(base_path, "estudiantes_colombia.csv")

    if not os.path.exists(file_path):
        st.error(f"No se encontró el archivo en: {file_path}")
        return pd.DataFrame()

    return pd.read_csv(file_path)

# Cargar datos
df = load_data()

# Si los datos se cargaron correctamente
if not df.empty:

    # Mostrar primeras y últimas filas
    st.header("🔍 Vista previa del dataset")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Primeras 5 filas")
        st.dataframe(df.head())

    with col2:
        st.subheader("Últimas 5 filas")
        st.dataframe(df.tail())

    # Mostrar info y describe
    st.header("📋 Resumen del dataset")

    if st.checkbox("Mostrar .info()"):
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        st.text(info_str)

    if st.checkbox("Mostrar .describe()"):
        st.dataframe(df.describe())

    # Seleccionar columnas
    st.header("📌 Seleccionar columnas específicas")
    columnas = st.multiselect(
        "Selecciona las columnas que deseas mostrar:",
        options=df.columns.tolist(),
        default=["nombre", "edad", "promedio"] if all(col in df.columns for col in ["nombre", "edad", "promedio"]) else df.columns[:3]
    )

    if columnas:
        st.dataframe(df[columnas])
    else:
        st.warning("⚠️ Selecciona al menos una columna para mostrar.")

    # Filtro por promedio
    if "promedio" in df.columns:
        st.header("🎯 Filtrar estudiantes por promedio")
        min_prom = float(df["promedio"].min())
        max_prom = float(df["promedio"].max())

        promedio_min = st.slider(
            "Promedio mínimo",
            min_value=min_prom,
            max_value=max_prom,
            value=min_prom,
            step=0.1
        )

        df_filtrado = df[df["promedio"] >= promedio_min]
        st.write(f"Estudiantes con promedio ≥ {promedio_min}:")
        st.dataframe(df_filtrado)
    else:
        st.warning("⚠️ La columna 'promedio' no se encuentra en el dataset.")
else:
    st.error("No se pudo cargar el dataset.")