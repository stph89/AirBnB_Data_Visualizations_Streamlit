# Importamos las librerias
import streamlit as st
import pandas as pd

# 1º Haver un boceto de cómo quieres que sea....hacer una plantilla con la estructura que va a tener (cabeceras, 
# descripción, contenedores y columnas, parte de visualizacion de gráficos, conclusiones) --->Imaginar como quieres que se vea


# Streamlit permite dividir tu contenido en contenedores y columnas
# Los contenedores dividen la página en secciones horizontales y las columnas permiten dividirla en secciones verticales. 
# Las columnas van dentro de los contenedores, pero no es necesario tener columnas en absoluto. Puedes tener sólo una columna en el centro. 

#Configurar la estructura principal de la página
##Definimos los contenedores o secciones que va mostrar
siteHeader = st.container()     ##Cabecera y descripción de nuestro proyecto de datascience
dataset = st.container()        ##Traemos los datos y pequeña introduccion/visualizacionón
features = st.container()       ##Contenedor características que hemos generado
modelTraining = st.container()  ##Contenedor para hablar o dar Ideas, generar y entrenar un modelo a futuro


## st.title() # corresponds to H1 heading
## st.header() # corresponds to H2 heading
## st.subheader() # corresponds to H3 heading
## st.text() v corresponds to text

#Contenedor Cabecera y descripcion
with siteHeader:
    st.title('Bienvenidos al Proyecto de datascience de alquiler vacacional en Sidney !')
    st.text('En este proyecto vamos a explorar los datos de la viviendas vacacionales \n'
            'que nos proporciona AirBnB')   ## Aqui parto el texto para que se vea bonito y no salga una barra horizontal
    st.text('Y vamos a visulaizar los datos en la ciudad de Sidney ... ')

#Contenedor para traer los datos y una pequeña introducción o visualización
with dataset:
    st.header('Dataset: Sidney AirBnB')
    st.text('Encontramos este dataset en http://insideairbnb.com/get-the-data/')
    df = pd.read_csv('../sydney_airbnb.csv')
    st.write(df.head())

    ## Visualization for my dataset.
    ### Nº de viviendas vacacionales en general por barrios
    st.subheader('Recoge el número de viviendas vacacionales')
    distribution_pickup = pd.DataFrame(df['neighbourhood'].value_counts())
    st.bar_chart(distribution_pickup)

##Contenedor características que hemos generado
with features:
    st.header('Las características que hemos creado')
    st.text('Permitirnos que tomemos una mirada a las características que hemos generado.')

##Concluiones para generar y entrenar un modelo de IA
with modelTraining:
    st.header('Model training')
    st.text('Concusiones: como podemos entrenar el modelo')
    st.text('Seleccionamos los hiperparametros para entrenar nuestro modelo')
  