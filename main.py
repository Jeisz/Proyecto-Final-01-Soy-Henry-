from fastapi import FastAPI
import os
import pandas as pd
import pyarrow.parquet as pq
from dateutil import parser

app = FastAPI()

# App de prueba 
@app.get("/")
def read_root():
    return {
        "Hola": "¡Bienvenido a mi Proyecto de   Individual  y presentación de endpints",
        "Te invito a": "Proyecto FastAPI - Sistema de Recomendaciones.",
        "Autor_proyecto": {
            "DataScientist": "Jeison Zapata2",
            "Mensaje": "Proyecto Individual N° 1 Soy Henry "
        },

    }
@app.get("/developer/{desarrollador}")

def developer(desarrollador):
    df = pd.read_parquet('./Notebooks/funcion_desarrollador')
    # Filtra el dataframe por desarrollador de interés
    data_filtrada = df[df['developer'] == desarrollador]
    # Calcula la cantidad de items por año
    cantidad_por_año = data_filtrada.groupby('year')['item_id'].count()
    # Calcula la cantidad de elementos gratis por año
    cantidad_gratis_por_año = data_filtrada[data_filtrada['price'] == 0.0].groupby('year')['item_id'].count()
    # Calcula el porcentaje de elementos gratis por año
    porcentaje_gratis_por_año = (cantidad_gratis_por_año / cantidad_por_año * 100).fillna(0).astype(int)

    result_dict = {
        'cantidad_por_año': str(cantidad_por_año),
        'porcentaje_gratis_por_año': str(porcentaje_gratis_por_año)
    }
    
    
    return result_dict
#//////////////////////////////////////////////////////////////////
@app.get("/userdata/{user_id}")

def userdata(user_id):
    #Cargar df formato parquet
    df_reviews = pd.read_parquet('./Datasets/df_reviews_1.parquet')
    df_gastos_items = pd.read_parquet('./Datasets/df_gastos_items.parquet')   
    df_genre_ranking = pd.read_parquet('./Datasets/df_genre_ranking.parquet')
    df_playtime_forever = pd.read_parquet('./Datasets/df_playtime_forever.parquet')   

    try:
        # Filtra por el usuario de interés
        usuario = df_reviews[df_reviews['user_id'] == user_id]
        
        # Calcula la cantidad de dinero gastado para el usuario de interés
        cantidad_dinero = float(df_gastos_items[df_gastos_items['user_id'] == user_id]['price'].iloc[0])
        
        # Busca el count_items para el usuario de interés
        count_items = int(df_gastos_items[df_gastos_items['user_id'] == user_id]['items_count'].iloc[0])
        
        # Filtra las recomendaciones del usuario de interés
        recomendaciones_usuario = usuario['reviews_recommend']
        
        # Calcula el total de recomendaciones realizadas por el usuario de interés
        total_recomendaciones = recomendaciones_usuario[recomendaciones_usuario == 'Recomendado'].count()
        
        # Calcula el total de reviews realizada por todos los usuarios
        total_reviews = len(df_reviews['user_id'].unique())
        
        # Calcula el porcentaje de recomendaciones realizadas por el usuario de interés
        porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100
        
        return {
            'cantidad_dinero': cantidad_dinero,
            'porcentaje_recomendacion': round(porcentaje_recomendaciones, 2),
            'total_items': count_items
        }
    except KeyError:
        return {
            'error': 'Usuario no encontrado en los DataFrames'
        }
@app.get("/user_for_genre/{genero}", response_model=dict)

def genre(genero):

    df_genre_ranking = pd.read_parquet('./Datasets/df_genre_ranking.parquet')
    
    try:
        # Busca el ranking para el género de interés
        rank = df_genre_ranking.loc[df_genre_ranking['genres'] == genero, 'ranking'].iloc[0]
    except IndexError:
        # Manejo del error: género no encontrado
        rank = None
    return {
        'rank': rank
    }

def userforgenre(genero):
    '''
    Esta función devuelve el top 5 de usuarios con más horas de juego en un género específico, junto con su URL de perfil y ID de usuario.
   l' (str): URL del perfil del usuario.
    '''
    df_playtime_forever = pd.read_parquet('./Datasets/df_playtime_forever.parquet')
    
    # Filtra el dataframe por el género de interés
    data_por_genero = df_playtime_forever[df_playtime_forever['genres'].str.contains(genero)]

    # Agrupa el dataframe filtrado por usuario y suma la cantidad de horas
    top_users = data_por_genero.groupby(['user_url', 'user_id'])['playtime_horas'].sum().nlargest(5).reset_index()

    # Crear una lista de diccionarios con la información de los usuarios
    top_users_list = []
    for index, row in top_users.iterrows():
        user_info = {
            'user_id': row['user_id'],
            'user_url': row['user_url']
        }
        top_users_list.append(user_info)

    # Crear el diccionario de retorno
    result = {
        'Top 5 usuarios para el género ' + genero: top_users_list
    }
    return result


@app.get("/best_developer_of_year/{year}")

def obtener_top_desarrolladores(df_playtime_forever, year):

    df_playtime_forever = pd.read_parquet('./Datasets/df_playtime_forever.parquet')

    # Filtrar las reseñas con comentarios positivos y recomendaciones verdaderas
    filtered_df = df_playtime_forever[df_playtime_forever['playtime_horas'] > 0]
    
    # Agrupar por desarrollador y calcular la suma de las recomendaciones
    developer_scores = filtered_df.groupby('user_id')['playtime_horas'].sum()
    
    # Ordenar los desarrolladores por puntuación en orden descendente
    sorted_developers = developer_scores.sort_values(ascending=False)
    
    # Seleccionar los tres primeros desarrolladores
    top_3_developers = sorted_developers.head(3)
    
    # Crear una lista de diccionarios con el formato deseado
    result = [{"Puesto {}: {}".format(i + 1, dev): score} for i, (dev, score) in enumerate(top_3_developers.items())]
    
    return result

def best_developer_year(year):
    df_playtime_forever = pd.read_parquet('./Datasets/df_playtime_forever.parquet')
    return obtener_top_desarrolladores(df_playtime_forever, year)