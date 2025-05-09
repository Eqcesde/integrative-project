import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 4")

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



# Crear un DataFrame de ejemplo
data = {
    'Nombre': ['Ana', 'Bob', 'Clara', 'David', 'Emma'],
    'Edad': [25, 30, 22, 35, 28],
    'Ciudad': ['Madrid', 'Barcelona', 'Sevilla', 'Valencia', 'Bilbao'],
    'Puntuación': [85, 90, 88, 92, 87]
}

df = pd.DataFrame(data, index=['a', 'b', 'c', 'd', 'e'])

# Título de la aplicación
st.title("Explora un DataFrame con .loc y .iloc")
st.write("Selecciona, filtra y modifica datos en un DataFrame interactivo.")

# Mostrar el DataFrame original
st.subheader("📊 DataFrame Original")
st.dataframe(df)

# Selección con .loc
st.subheader("🔍 Selección con .loc")
loc_row = st.text_input("Ingresa el índice de la fila (ej. 'a', 'b'):", value='a')
loc_col = st.multiselect("Selecciona columnas:", df.columns.tolist(), default=['Nombre', 'Edad'])

if loc_row in df.index:
    st.write("Resultado de df.loc[loc_row, loc_col]:")
    st.write(df.loc[loc_row, loc_col])
else:
    st.warning("El índice ingresado no existe en el DataFrame.")

# Selección con .iloc
st.subheader("🔎 Selección con .iloc")
row_pos = st.number_input("Posición de fila (0 a 4):", min_value=0, max_value=4, step=1)
col_pos = st.multiselect("Posiciones de columnas (0:Nombre, 1:Edad, 2:Ciudad, 3:Puntuación):", [0, 1, 2, 3], default=[0, 1])

try:
    st.write("Resultado de df.iloc[row_pos, col_pos]:")
    st.write(df.iloc[row_pos, col_pos])
except Exception as e:
    st.error(f"Error al usar iloc: {e}")

# Filtro con condición
st.subheader("📌 Filtrar por condición con .loc")
edad_min = st.slider("Edad mínima:", min_value=0, max_value=100, value=25)
df_filtrado = df.loc[df['Edad'] >= edad_min]
st.write(f"Filas con Edad >= {edad_min}")
st.dataframe(df_filtrado)

# Modificación de datos
st.subheader("✏ Modificación de datos")
row_mod = st.selectbox("Selecciona fila a modificar (por índice):", df.index)
col_mod = st.selectbox("Selecciona columna a modificar:", df.columns)
nuevo_valor = st.text_input(f"Nuevo valor para {col_mod} en la fila {row_mod}:")

if st.button("Modificar valor"):
    try:
        df.loc[row_mod, col_mod] = type(df.loc[row_mod, col_mod])(nuevo_valor)
        st.success(f"Valor modificado: {row_mod}, {col_mod} = {nuevo_valor}")
    except Exception as e:
        st.error(f"Error al modificar valor: {e}")

    # Mostrar DataFrame actualizado
    st.subheader("📋 DataFrame actualizado")
    st.dataframe(df)