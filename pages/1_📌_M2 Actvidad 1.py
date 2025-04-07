import pandas as pd
import streamlit as st
import sqlite3
import json
import numpy as np
import firebase_admin

from firebase_admin import credentials, firestore

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 1")

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

st.title("Actividad 1 - Creacion de DateFrames")
st.header("Descripción de la actividad")
st.markdown("esta actividad es para Familiarizarse con la creación de DataFrames en Pandas y mostrarlos usando Streamlit.")

libros = {
    "título": ["Cien años de soledad", "1984", "El Principito", "Matar a un ruiseñor"],
    "autor": ["Gabriel García Márquez", "George Orwell", "Antoine de Saint-Exupéry", "Harper Lee"],
    "año de publicación": [1967, 1949, 1943, 1960],
    "género": ["Realismo mágico", "Distopía", "Fábula", "Ficción histórica"]
}
df_libros = pd.DataFrame(libros)

ciudades = [
    {"nombre": "París", "población": 2148000, "país": "Francia"},
    {"nombre": "Tokio", "población": 13960000, "país": "Japón"},
    {"nombre": "Nueva York", "población": 8419000, "país": "Estados Unidos"},
    {"nombre": "Buenos Aires", "población": 2890000, "país": "Argentina"}
]
df_ciudades = pd.DataFrame(ciudades)

productos = [
    ["Laptop", 1200, 15],
    ["Smartphone", 800, 30],
    ["Tablet", 500, 25],
    ["Monitor", 300, 20]
]
df_productos = pd.DataFrame(productos, columns=["Nombre", "Precio", "Cantidad en Stock"])

nombres = pd.Series(["Ana", "Carlos", "Beatriz", "David"])
edades = pd.Series([25, 30, 22, 35])
ciudades_personas = pd.Series(["Madrid", "Buenos Aires", "París", "México"])

df_personas = pd.DataFrame({
    "Nombre": nombres,
    "Edad": edades,
    "Ciudad": ciudades_personas
})

def cargar_datos():
    return pd.read_excel("data.xlsx", engine="openpyxl")

data = [
    {"nombre": "Juan Perez", "correo": "juan@example.com"},
    {"nombre": "Maria Gomez", "correo": "maria@example.com"},
    {"nombre": "Carlos Lopez", "correo": "carlos@example.com"}
]

with open("data.json", "w") as file:
    json.dump(data, file, indent=4)

url = "https://www.datos.gov.co/resource/sbwg-7ju4.csv"


conn = sqlite3.connect('estudiantes.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS estudiantes (
        nombre TEXT,
        calificacion REAL
    )
''')
cursor.execute("SELECT COUNT(*) FROM estudiantes")
if cursor.fetchone()[0] == 0:
    datos = [
        ("Ana Martínez", 8.9),
        ("Carlos Pérez", 7.5),
        ("Lucía Gómez", 9.3)
    ]
    cursor.executemany("INSERT INTO estudiantes (nombre, calificacion) VALUES (?, ?)", datos)
    conn.commit()

data = np.array([
    [1, 'Ana', 85.5],
    [2, 'Luis', 90.0],
    [3, 'Carla', 78.3]
])

columnas = ['ID', 'Nombre', 'Puntaje']

cred = credentials.Certificate("usuarios.json")  # Ruta a tu clave
firebase_admin.initialize_app(cred)
db = firestore.client()

usuarios_ref = db.collection('usuarios')
docs = usuarios_ref.stream()

datos = []
for doc in docs:
    data = doc.to_dict()
    datos.append(data)



df_dataframe = pd.DataFrame(datos)

df_np = pd.DataFrame(data, columns=columnas)

df_url = pd.read_csv(url, sep=None, engine='python', encoding='latin1', on_bad_lines='skip')

df_json = pd.read_json("data.json")

df_csv = pd.read_csv("data.csv")

df_sql = pd.read_sql("SELECT * FROM estudiantes", conn)

st.write("## DataFrame de Libros")
st.dataframe(df_libros)

st.write("## Información de Ciudades")
st.dataframe(df_ciudades)

st.write("## Productos en Inventario")
st.dataframe(df_productos)

st.write("## Información de Personas")
st.dataframe(df_personas)

st.write("## Datos desde CSV")
st.dataframe(df_csv)

st.header("Datos desde Excel")
df = cargar_datos()
st.dataframe(df)

st.header("Datos de Usuarios desde JSON")
st.dataframe(df_json)

st.header("Datos desde URL")
st.dataframe(df_url)

st.title("Datos desde SQLite")
st.dataframe(df_sql)

st.title("Datos desde NumPy")
st.dataframe(df_np)

st.title("Datos desde Firebase")
st.dataframe(df_dataframe)