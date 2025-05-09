import streamlit as st
import pandas as pd
import numpy as np
import random
from faker import Faker 


# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 3")

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

# Título de la app
st.title("📘 Proyecto en Google Colab")

# Descripción del proyecto
st.markdown("""
¡Bienvenido! Aquí puedes acceder al cuaderno de Google Colab donde se desarrolla el análisis completo del proyecto.
""")

# URL de Google Colab
colab_url = "https://colab.research.google.com/drive/10_sU48HthEJpKGa75YC6J3fe6Z3jZoQu?usp=sharing"  # Reemplaza con tu enlace real

# HTML personalizado con logo e interactividad
st.markdown(f"""
    <style>
    .colab-button {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        background-color: #F9AB00;
        color: black;
        font-weight: bold;
        font-size: 18px;
        padding: 12px 24px;
        border-radius: 12px;
        text-decoration: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }}
    .colab-button:hover {{
        background-color: #FFCC00;
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        text-decoration: none;
    }}
    </style>

    <div style="text-align: center; margin-top: 30px;">
        <a href="{colab_url}" target="_blank" class="colab-button">
            <img src="https://upload.wikimedia.org/wikipedia/commons/3/38/Google_Colaboratory_Logo.svg" alt="Colab Logo" width="32" height="32">
            Abrir en Google Colab
        </a>
    </div>
""", unsafe_allow_html=True)


# Configurar Faker para Colombia
fake = Faker('es_CO')
np.random.seed(42)
random.seed(42)
fake.seed_instance(42)

# Crear datos simulados
n = 50
data = {
    'id': range(1, n + 1),
    'nombre': [fake.first_name() for _ in range(n)],
    'edad': np.random.randint(18, 81, n),
    'ciudad': random.choices(
        ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 'Bucaramanga', 'Pereira'], k=n
    ),
    'salario': np.random.randint(1000000, 10000001, n).astype(float),
    'nivel_educativo': random.choices(
        ['Primaria', 'Secundaria', 'Técnico', 'Universitario', 'Posgrado'], k=n
    ),
    'estado_civil': random.choices(
        ['Soltero', 'Casado', 'Unión libre', 'Divorciado', 'Viudo'], k=n
    ),
    'fecha_registro': pd.date_range(start='2023-01-01', end='2024-12-31', periods=n),
    'tiene_vehiculo': random.choices([True, False], k=n)
}
deptos = {
    'Bogotá': 'Cundinamarca',
    'Medellín': 'Antioquia',
    'Cali': 'Valle del Cauca',
    'Barranquilla': 'Atlántico',
    'Cartagena': 'Bolívar',
    'Bucaramanga': 'Santander',
    'Pereira': 'Risaralda'
}
df = pd.DataFrame(data)
df['departamento'] = df['ciudad'].map(deptos)
df.loc[5:7, 'salario'] = np.nan
df.loc[10:12, 'nivel_educativo'] = np.nan
df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])

# -------------------
# STREAMLIT APP
# -------------------

st.title("Explorador de datos con filtros - Colombia 🇨🇴")

st.sidebar.header("Filtros disponibles")

# Filtro 1: Rango de edad
edad_min, edad_max = st.sidebar.slider("Rango de edad", 18, 80, (18, 80))
df_filtrado = df[(df['edad'] >= edad_min) & (df['edad'] <= edad_max)]

# Filtro 2: Selección de ciudad
ciudades = st.sidebar.multiselect("Ciudad", options=df['ciudad'].unique(), default=df['ciudad'].unique())
df_filtrado = df_filtrado[df_filtrado['ciudad'].isin(ciudades)]

# Filtro 3: Rango de salario
salario_min = int(df['salario'].min(skipna=True))
salario_max = int(df['salario'].max(skipna=True))
rango_salario = st.sidebar.slider("Rango de salario", salario_min, salario_max, (salario_min, salario_max))
df_filtrado = df_filtrado[(df_filtrado['salario'] >= rango_salario[0]) & (df_filtrado['salario'] <= rango_salario[1])]

# Filtro 4: Nivel educativo (manejo de nulos incluido)
niveles = st.sidebar.multiselect("Nivel educativo", options=df['nivel_educativo'].dropna().unique(), default=df['nivel_educativo'].dropna().unique())
df_filtrado = df_filtrado[df_filtrado['nivel_educativo'].isin(niveles)]

# Filtro 5: Estado civil
estado_civil = st.sidebar.multiselect("Estado civil", options=df['estado_civil'].unique(), default=df['estado_civil'].unique())
df_filtrado = df_filtrado[df_filtrado['estado_civil'].isin(estado_civil)]

# Filtro 6: Rango de fechas
fecha_inicio = st.sidebar.date_input("Desde", df['fecha_registro'].min())
fecha_fin = st.sidebar.date_input("Hasta", df['fecha_registro'].max())
df_filtrado = df_filtrado[(df_filtrado['fecha_registro'] >= pd.to_datetime(fecha_inicio)) &
                          (df_filtrado['fecha_registro'] <= pd.to_datetime(fecha_fin))]

# Filtro 7: Tiene vehículo
vehiculo = st.sidebar.selectbox("¿Tiene vehículo?", options=["Todos", "Sí", "No"])
if vehiculo == "Sí":
    df_filtrado = df_filtrado[df_filtrado['tiene_vehiculo'] == True]
elif vehiculo == "No":
    df_filtrado = df_filtrado[df_filtrado['tiene_vehiculo'] == False]

# Filtro 8: Departamento
departamento = st.sidebar.multiselect("Departamento", options=df['departamento'].unique(), default=df['departamento'].unique())
df_filtrado = df_filtrado[df_filtrado['departamento'].isin(departamento)]

# Filtro 9: Filtrar personas con salario nulo (para análisis de faltantes)
incluir_nulos_salario = st.sidebar.checkbox("Incluir registros con salario nulo")
if not incluir_nulos_salario:
    df_filtrado = df_filtrado[df_filtrado['salario'].notnull()]

# Filtro 10: Búsqueda por nombre
nombre_busqueda = st.sidebar.text_input("Buscar por nombre")
if nombre_busqueda:
    df_filtrado = df_filtrado[df_filtrado['nombre'].str.contains(nombre_busqueda, case=False)]

# Mostrar resultados
st.subheader(f"Resultados: {len(df_filtrado)} registros encontrados")
st.dataframe(df_filtrado.reset_index(drop=True))

# Estadísticas básicas
st.subheader("Resumen estadístico")
st.write(df_filtrado.describe(include='all'))