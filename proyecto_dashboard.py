# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 19:14:09 2024

@author: Jose Alonso
"""

import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt


st.title("Monitoreo de la actividad sísmica en el Perú ")

@st.cache_data
def get_data(filename)
    # Leer el archivo Excel en un DataFrame
    df = pd.read_excel(filename)
    
    # Eliminar ID
    df.drop('ID', axis = 1, inplace= True)
    
    # Crear columna DateTime FECHA_HORA_UTC
    df['FECHA_HORA_UTC'] = df['FECHA_UTC'].astype(str) + df['HORA_UTC'].astype(str).str.zfill(6)
    df['FECHA_HORA_UTC'] = pd.to_datetime(df['FECHA_HORA_UTC'], format='%Y%m%d%H%M%S')
    
    # Eliminar columnas FECHA_UTC y HORA_UTC
    df.drop(['FECHA_UTC', 'HORA_UTC'], axis=1, inplace = True)
    
    # Crear columna DateTime FECHA_HORA_UTC
    df['FECHA_CORTE'] = pd.to_datetime(df['FECHA_CORTE'].astype(str), format='%Y%d%m')
    
    return df

df = get_data("Catalogo1960_2023.xlsx")

# Mostrar los primeros 10 registros del DataFrame
st.write("Primeros 5 registros:")
st.write(df.head())


# Mostrar estadísticas descriptivas del DataFrame
st.write("Estadísticas descriptivas de los valores numéricos:")
st.write(df.describe())


if 'MAGNITUD' in df.columns:
       # Crear gráfico de líneas de la columna 'magnitud'
       st.write("Gráfico de Líneas de la columna 'magnitud':")
       fig, ax = plt.subplots()
       ax.plot(df['MAGNITUD'])
       ax.set_xlabel('Índice')
       ax.set_ylabel('Magnitud')
       st.pyplot(fig)
else:
       st.write("La columna 'magnitud' no está presente en el conjunto de datos.")
       
# Obtener el valor mínimo y máximo de la columna datetime
valor_minimo = df['FECHA_HORA_UTC'].min().to_pydatetime()
valor_maximo = df['FECHA_HORA_UTC'].max().to_pydatetime()

valor_minimo = valor_minimo.replace(hour=0, minute=0, second=0)
valor_maximo = valor_maximo.replace(hour=23, minute=59, second=59)

# Seleccionar el rango de fechas a visualizar
st.subheader("Sismos fuertes - Magnitud mayor a 6.1")
st.write('Ingresa rango de fechas:')
range_dates = st.slider("Ver casos ocurridos entre",
                        min_value=valor_minimo,
                        max_value=valor_maximo,
                        value=(valor_minimo,valor_maximo),
                        format="YYYY-MM-DD")

# Filtrar el DataFrame utilizando el rango de fechas seleccionado
df_filtrado = df[(df['FECHA_HORA_UTC'] >= pd.Timestamp(range_dates[0])) & (df['FECHA_HORA_UTC'] <= pd.Timestamp(range_dates[1]))]
df_filtrado = df_filtrado.loc[df['MAGNITUD']>=6.1]
st.map(df_filtrado,latitude='LATITUD',longitude='LONGITUD')

# Seleccionar el rango de fechas a visualizar
st.subheader("Sismos ocurridos por año")
valor_maximo = df['FECHA_HORA_UTC'].max().to_pydatetime()

st.write('Ingresar año de búsqueda:')
search_year = st.slider("Ver casos ocurridos el año",
                        min_value=valor_minimo,
                        max_value=valor_maximo,
                        format="YYYY")

# Filtrar el DataFrame utilizando el rango de fechas seleccionado
st.map(df.loc[df['FECHA_HORA_UTC'].dt.year == search_year.year],latitude='LATITUD',longitude='LONGITUD')
