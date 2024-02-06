
  <p align="center">
  <img src="https://github.com/Jeisz/Proyecto-Final-01-Soy-Henry-/assets/128953226/59b1396f-f12f-45d2-8af4-9bbd24b33c39" alt="Purple Sky Profile Header"/>
</p>


  ![Steam 1](https://github.com/Jeisz/Proyecto-Final-01-Soy-Henry-/assets/128953226/51226b14-e84b-41e9-879b-7597fa4caa7d)

Proyecto Steam: Análisis y Recomendación de Juegos
Introducción
Este emocionante proyecto simula el papel de un MLOps Engineer, fusionando las habilidades de un Data Engineer y un Data Scientist, todo ello en el contexto de la plataforma multinacional de videojuegos Steam. Nuestro objetivo es desarrollar un Producto Mínimo Viable (PMV) que ofrezca una API implementada en la nube y aplique dos modelos de Machine Learning:

Análisis de Sentimientos: Evaluaremos los comentarios de los usuarios sobre los juegos, determinando si son positivos o negativos.
Recomendación de Juegos: Basándonos en el nombre de un juego o en las preferencias de un usuario, sugeriremos títulos afines.
Contexto
Steam, creada por Valve Corporation, es una plataforma líder en la distribución digital de videojuegos. Desde su lanzamiento en septiembre de 2003, ha evolucionado para incluir no solo los juegos de Valve, sino también títulos de terceros. Con más de 325 millones de usuarios y un catálogo de más de 25,000 juegos, Steam es un referente en la industria.

Es relevante mencionar que las estadísticas disponibles hasta 2017 provienen de SteamSpy, ya que en 2018 Steam modificó la forma de obtener datos, lo que afectó la precisión de las cifras.

Datos
Para este proyecto, contamos con tres archivos JSON:

australian_user_reviews.json: Este conjunto de datos contiene comentarios de usuarios sobre los juegos que consumen. Además, incluye información sobre si recomiendan o no un juego, emoticones utilizados y estadísticas de utilidad de los comentarios. También se proporciona el ID del usuario y el ID del juego al que se refieren.
australian_users_items.json: Aquí encontramos detalles sobre los juegos que juegan los usuarios, incluyendo el tiempo acumulado que cada uno ha dedicado a un juego específico.
Transformaciones y Análisis de Sentimiento en el Proyecto Steam
Transformaciones de Datos (ETL)
En este emocionante proyecto, nos sumergimos en la extracción, transformación y carga (ETL) de tres conjuntos de datos entregados. Dos de ellos presentaban anidaciones, es decir, columnas con diccionarios o listas de diccionarios. Para abordar esto, aplicamos diversas estrategias para transformar las claves de esos diccionarios en columnas legibles. Además, rellenamos valores nulos en variables críticas para el proyecto y eliminamos columnas con excesivos nulos o que no aportaban significativamente. Todo esto se hizo con el objetivo de optimizar el rendimiento de la API y considerando las limitaciones de almacenamiento en el despliegue. La poderosa librería Pandas fue nuestra aliada en estas transformaciones.

Los detalles específicos de cada ETL se encuentran en los archivos:

ETL output_steam_games
ETL australian_users_items
ETL australian_user_reviews
Ingeniería de Características: Análisis de Sentimiento
Uno de los requerimientos clave fue aplicar un análisis de sentimiento a las reseñas de los usuarios. Para lograrlo, creamos una nueva columna llamada ‘sentiment_analysis’, que reemplaza la columna original que contenía las reseñas. Esta nueva columna clasifica los sentimientos de los comentarios en la siguiente escala:

0: Si es negativo.
1: Si es neutral o no tiene reseña.
2: Si es positivo.
Dado que nuestro objetivo es realizar una prueba de concepto, aplicamos un análisis de sentimiento básico utilizando TextBlob, una biblioteca de procesamiento de lenguaje natural (NLP) en Python. Esta metodología asigna un valor numérico a un texto (en este caso, los comentarios de los usuarios sobre un juego específico), representando si el sentimiento expresado es negativo, neutral o positivo.
Análisis Exploratorio de Datos y Modelos de Recomendación en el Proyecto Steam
Análisis Exploratorio de Datos (EDA)
En esta emocionante fase, nos sumergimos en los tres conjuntos de datos sometidos a ETL. Nuestro objetivo: identificar las variables que serán fundamentales para la creación del modelo de recomendación. Para lograrlo, utilizamos la poderosa librería Pandas para manipular los datos y las herramientas de visualización Matplotlib y Seaborn.

En particular, para el modelo de recomendación, tomamos una decisión clave: construir un dataframe específico. Este dataframe incluye el ID del usuario que realizó las reseñas, los nombres de los juegos sobre los cuales se comentó y una columna de rating construida a partir de la combinación del análisis de sentimiento y las recomendaciones de juegos.

Todo este proceso está documentado en nuestra Jupyter Notebook llamada EDA.

Modelos de Aprendizaje Automático
Creamos dos modelos de recomendación, cada uno generando una lista de 5 juegos. Estos modelos pueden recibir como entrada el nombre de un juego o el ID de un usuario.

Modelo Ítem-Ítem: Este modelo se basa en relaciones entre juegos. Dado un juego, evaluamos su similitud con otros títulos y recomendamos aquellos similares.
Modelo Usuario-Juego: Aquí aplicamos un filtro usuario-juego. Tomamos un usuario, encontramos usuarios similares y recomendamos juegos que a esos usuarios les gustaron.
Ambos modelos utilizan algoritmos basados en la memoria, abordando el problema del filtrado colaborativo utilizando toda la base de datos. Buscamos usuarios similares al usuario activo (es decir, aquellos a quienes queremos recomendar) y utilizamos sus preferencias para predecir las valoraciones del usuario activo.

Para medir la similitud entre juegos (item_similarity) y entre usuarios (user_similarity), empleamos la similitud del coseno. Esta medida evalúa la similitud entre dos vectores en un espacio multidimensional, siendo fundamental en sistemas de recomendación y análisis de datos.
API para el Proyecto Steam: Funciones y Recomendaciones
Funciones de la API
1. userdata
Parámetro: user_id
Descripción: Devuelve información relevante sobre un usuario específico:
Cantidad de dinero gastado por el usuario.
Porcentaje de recomendaciones que realizó en relación a la cantidad total de reseñas analizadas.
Número de elementos (juegos) consumidos por el usuario.
2. countreviews
Parámetros: Dos fechas (rango de consulta)
Descripción: Proporciona estadísticas sobre las reseñas realizadas entre las fechas especificadas:
Cantidad total de usuarios que realizaron reseñas.
Porcentaje de recomendaciones positivas (valor “True”) hechas por los usuarios.
3. género
Parámetro: Género de videojuego
Descripción: Calcula la posición de ese género en un ranking basado en las horas jugadas por los usuarios.
4. userforgenre
Parámetro: Género de videojuego
Descripción: Proporciona el top 5 de usuarios con más horas de juego en el género especificado, incluyendo sus IDs y URLs de perfil.
5. desarrollador
Parámetro: Nombre de la empresa desarrolladora
Descripción: Ofrece información sobre la empresa:
Cantidad total de elementos (juegos) desarrollados por esa empresa.
Porcentaje de contenido gratuito por año en comparación con el total desarrollado.
6. sentiment_analysis
Parámetro: Año de lanzamiento de un juego
Descripción: Devuelve una lista con la cantidad de registros de reseñas de usuarios categorizados según análisis de sentimiento (Negativo, Neutral y Positivo).
7. recomendacion_juego
Parámetro: Nombre de un juego
Descripción: Recomienda 5 juegos similares al ingresado.
8. recomendacion_usuario
Parámetro: ID de un usuario
Descripción: Sugiere 5 juegos para ese usuario, considerando similitudes entre usuarios.
