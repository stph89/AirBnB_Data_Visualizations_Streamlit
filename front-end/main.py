# Importamos las librerias
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk    # para la función pydeck
from streamlit_folium import st_folium
import folium
import seaborn as sns             # Importamos seaborn
import matplotlib
import matplotlib.pyplot as plt   # Importamos los paquetes de librias de matplotlib para las gráficas
import plotly.graph_objects as go   #Importamos para funcion grafica chart_lyne
import mpld3
import base64       #Para el logo
import streamlit.components.v1 as components
import plotly.express as px       #Graficas interactivas para scatterplot
from plotly.subplots import make_subplots   #Para los subplot de los scatterplots
from PIL import Image       # Importamos para cargar imagenes
import tablas       #Importamos tablas para usar el metodo para graficar la tabla interactiva
import streamlit as st


# SETTING PAGE CONFIG PARA MODO ANCHO Y AÑADIENDO UN TÍTULO Y UN FAVICON A NUESTRA PÁGINA
st.set_page_config(layout="wide", page_title="Sidney AirBnB Data Demo", page_icon=":hotel:")


# 1º Haver un boceto de cómo quieres que sea....hacer una plantilla con la estructura que va a tener (cabeceras, 
# descripción, contenedores y columnas, parte de visualizacion de gráficos, conclusiones) --->Imaginar como quieres que se vea

# Comienza el programa
def main():

    # Configuracion de css
    st.markdown('<style>' + open('./styles.css').read() + '</style>', unsafe_allow_html=True)

# Streamlit permite dividir tu contenido en contenedores y columnas
# Los contenedores dividen la página en secciones horizontales y las columnas permiten dividirla en secciones verticales. 
# Las columnas van dentro de los contenedores, pero no es necesario tener columnas en absoluto. Puedes tener sólo una columna en el centro. 

#Configurar la estructura principal de la página
##Definimos los contenedores o secciones que va mostrar
siteHeader = st.container()     ##Cabecera y descripción de nuestro proyecto de datascience
dataset = st.container()        ##Traemos los datos y pequeña introduccion/visualizacionón
features = st.container()       ##Contenedor características que hemos generado
features2 = st.container()      ##Contenedor para gráficas de scatterplots
conlusions = st.container()     ##Conclusiones y como podemos llegar a entrenar un modelo


## st.title() # corresponds to H1 heading
## st.header() # corresponds to H2 heading
## st.subheader() # corresponds to H3 heading
## st.st.subheader()text() v corresponds to text

#Contenedor Cabecera y descripcion
with siteHeader:
    LOGO_IMAGE = "Logo_Sidney_AirBnB.png"
    st.markdown(
        """
        <style>
        .container {
            display: flex;
        }
        .logo-text {
            font-weight:700 !important;
            font-size:50px !important;
            color: #f9a01b !important;
            padding-top: 75px !important;
        }
        .logo-img {
            float:right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="container">
            <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
            <p class="logo-text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sidney AirBnB Data Visualizer Demo!</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)

    with col1:
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.subheader('En este proyecto nos centramos en la exploración \n\n')
        st.subheader('y visualización de datos obtenidos de viviendas \n\n')
        st.subheader('de uso vacacional en la ciudad de Sidney (Australia), \n\n')
        st.subheader('a través del servicio que nos ofrece la plataforma  \n\n')      ## Aqui parto el texto para que se vea bonito y no salga una barra horizontal 
        st.subheader('AirBnB durante los años 2011 y 2019....\n\n\n ')
    
    with col2:
        #st.image("https://static.streamlit.io/examples/dog.jpg")
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        image = Image.open('opera.jpg')
        new_image = image.resize((700, 600))
        st.image(new_image)

    #Contenedor para traer los datos y una pequeña introducción o visualización
    with dataset:
        df = pd.read_csv('../data/sydney_airbnb.csv')
        df_map = df[["latitude", "longitude"]]
    
        st.header("🖱️ Tabla Interactiva Sidney AirBnB")
        st.write("Vamos a explorar los datos de AirBnB de la ciudad de Sidney:")
        st.write("Haz click en una fila de la tabla debajo para visualizar los datos de tu interés!")

        data = pd.read_csv('../data/groupby2.csv')

        selection = tablas.aggrid_interactive_table(df=data)

        st.write("*Los valores corresponden a los valores medio de cada categoría de datos seleccionados.")
        st.write("Número total de inmuebles AirBnB del data set = 36.662")
        st.markdown('Encontramos este dataset en http://insideairbnb.com/get-the-data/')

##Contenedor características que hemos generado. Mapas
with features:
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.header('Las primeras características que visualizamos')
    st.text('Permitirnos que tomemos una mirada más generica a las características de los datos según el conteo de viviendas y de precio según el barrio.')

    df_filtrado=df.drop( ["neighbourhood_group"] ,axis = 1 )
    df_fil_noches_hc=df_filtrado[(df_filtrado["price"]<=1500) & 
                             (df_filtrado["minimum_nights"]<=100) & 
                             (df_filtrado["calculated_host_listings_count"]<=75)]

    groupby = df_fil_noches_hc.groupby(['room_type','neighbourhood']).aggregate('mean')
    groupby = groupby.reset_index(level=0)
    groupby = groupby.reset_index(level=0)

    #Barplot Precios medios por barrio por tipo de habitación.
    fig_bar = px.bar(groupby, x='neighbourhood', y='price', color='room_type', hover_name='room_type')
    st.plotly_chart(fig_bar, use_container_width=True) 

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.markdown("<h5 style='text-align:center; color: white;'> El mayor número de inmuebles son del tipo casa entera, siendo los inmuebles con mayor precio de alquiler y mayormente situados cerca a la costa de Sidney. Se observan 3 barrios con mayor número de inmuebles. El barrio con mayor número de inmuebles es Sidney, seguido de Waberly y Randwick; cercanos al centro y la costa. </h5>", unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")


    #Countplot: Conteo inmuebles por barrio por tipo de habitación.
    fig_countplot = px.histogram(df_fil_noches_hc, x='neighbourhood', color='room_type', hover_name='room_type')
    st.plotly_chart(fig_countplot, use_container_width=True)    

    # Chart_line o gráfico de evolución precio por año y barrio
    df_neig_year = pd.read_csv("../data/neig_year.csv")

    clist = df_neig_year["neighbourhood"].unique().tolist()

    neighbourhoods = st.multiselect("Select neighbourhood", clist, default=df_neig_year['neighbourhood'].drop_duplicates().sort_values())
    #st.header("You selected: {}".format(", ".join(neighbourhoods)))

    dfs = {neighbourhood: df_neig_year[df_neig_year["neighbourhood"] == neighbourhood] for neighbourhood in neighbourhoods}
    
###
### cOLUMNA DEL GRAFICO Y DESCRIPCION CON COMENTARIOS...IZQUIERDA: GRAFICO Y DERECHA: DESCRIPCION
###

    display_goScatter, col_descrip = st.columns([4,  2])

    with display_goScatter:
        fig = go.Figure()
        for neighbourhood, df_neig_year in dfs.items():
            fig = fig.add_trace(go.Scatter(x=df_neig_year["last_review_year_date"], y=df_neig_year["price"], name=neighbourhood))
            fig.update_layout(
            autosize=False,
            width=800,
            height=600,)

        st.plotly_chart(fig)

    with col_descrip:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.markdown("<h5 style='color: white;'> Gráfica que nos muestra la evolución de los precios promedio por año según cada barrio. No todos los barrios tienen todos los años disponibles </h5>", unsafe_allow_html=True)
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.markdown("<h5 style='color: white;'> El precio medio de alquiler en la ciudad de Sidney es de $187 </h5>", unsafe_allow_html=True)


    st.subheader('Muestra las viviendas listadas según el barrio')

    # Para poner un icon de una url (NO FUNCIONA!!!)
    #icon = folium.features.CustomIcon('https://fontawesome.com/icons/alien?s=duotone', icon_size=(24, 24))

    # Creamos dos columnas dentro del contenedor
    selection_col, display_col  = st.columns(2)
    
    with selection_col:
        ## Lista de opciones por barrio ordenados alfabeticamente
        option_neighbourhood = st.selectbox(
        'Elige que barrio quieres mostrar?', df['neighbourhood'].drop_duplicates().sort_values()
        )

        st.write('Seleccionaste:', option_neighbourhood)

    with display_col:
        # Acotamos el mapa a un barrio en concreto
        df_neighbourdhood = df["neighbourhood"] == option_neighbourhood     # Entradas que cumplen la condición. En este caso, el neighbourhood que buscamos mapear
        df_map_neighbourdhood = df[df_neighbourdhood]                   # Dataframe con todos las columnas que cumplen la condición de neighbourhood
        st.map(df_map_neighbourdhood[["latitude", "longitude"]])

    st.subheader('Muestra las viviendas sobre mapa condicionado a 4 variables')
    
    ## Multiseleccion para el barrio
    options_neighbourhood = st.multiselect(
    'Elige el barrio que quieres mostrar?',
    df['neighbourhood'].drop_duplicates().sort_values(), default=df['neighbourhood'].drop_duplicates().sort_values())   #Por defecto muestra Sidney

    # Creamos dos columnas dentro del contenedor
    columna_selectores, columna_map  = st.columns([1,  3])
    
    with columna_selectores:
        ## Multiseleccion para el tipo de habitación
        options_roomType = st.multiselect(
        'Elige el tipo de habitación que quieres mostrar?',
        df['room_type'].drop_duplicates().sort_values(), default=df['room_type'].drop_duplicates().sort_values())   #Por defecto saladrá Entire home/apt

        ## Slidebar de precios y mínimo de noches
        precios_sidney = st.slider("Precio vivienda:", 1, 25)
        minimum_nights = st.slider("Minimo de noches:", 1, 30)
    
    with columna_map:
        items = folium.Map(
            location=[-33.86785,151.20732],
            zoom_start=12,
            tiles='Stamen Terrain'
            )
            
        #Filtramos el mapa por las 4 condiciones escogidas
        ##Filtrados por elementos en una lista (options_neighbourhood)
        df_fil_options_neighbourhood = df[df.neighbourhood.isin(options_neighbourhood)]

        ##Filtrados de elementos room_type dentro del datafra filtrado por barrio
        df_fil_options = df_fil_options_neighbourhood[df_fil_options_neighbourhood.room_type.isin(options_roomType)]  
        
        for index, row in df_fil_options_neighbourhood.iterrows():
            if precios_sidney>=row['price'] and minimum_nights>=row['minimum_nights']:
                tooltip = f" Nombre: {row['name']}, Nº reviews: {row['number_of_reviews']}, Nº mín noches: {row['minimum_nights']}, Price: {row['price']}"
                items.add_child(folium.Marker((row['latitude'], row['longitude']), popup=f" Nombre: {row['name']}, Nº reviews: {row['number_of_reviews']}, Nº mín noches: {row['minimum_nights']}, Price: {row['price']}", tooltip=tooltip, icon=folium.Icon(icon="hotel", prefix='fa', color='pink')).add_to(items))
        st_data =st_folium(items, width=1000)
    
    ## Mapa en 3D
    # Mapa que hace un conteo según las concentración de las coordenadas que presenta el dataframe
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=-33.8567844,
            longitude=151.2152967,
            zoom=11,
            pitch=50,
        ),
        layers=[            
            pdk.Layer(
                'HexagonLayer',
                data=df_map,
                get_position='[longitude, latitude]',
                radius=50,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df_map,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=50,
            ),
        ],
    )) 


##Gráficos interactivos con scatterplots
with features2:
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.header('Scatterplots más interesantes')
    st.subheader('Veamos unos scatterplots por barrios y tipo de habitación')

    df_filtrado=df.drop( ["neighbourhood_group"] ,axis = 1 )
    df_fil_noches_hc=df_filtrado[(df_filtrado["price"]<=1500) & 
                                (df_filtrado["minimum_nights"]<=100) & 
                                (df_filtrado["calculated_host_listings_count"]<=75)]

    #Las gráficas más segun la relacion de correlación mas fuerte con un muestro por barrios
    st.text('Vemos las 4 primeras graficas que relacionan barrios por colores')

    fig1 = px.scatter(df_fil_noches_hc, x='longitude', y='price', color='neighbourhood', hover_name='neighbourhood')
    fig2 = px.scatter(df_fil_noches_hc, x='longitude', y='latitude', color='room_type', hover_name='room_type')
    fig3 = px.scatter(df_fil_noches_hc, x='longitude', y='latitude', color='neighbourhood', hover_name='neighbourhood')
    fig4 = px.scatter(df_fil_noches_hc, x='price', y='latitude', color='neighbourhood', hover_name='neighbourhood')
    
    ## Tenemos qu arreglar que salga en 2 row y 2 columns. NO SALEEE

    # Creamos dos columnas dentro del contenedor..SALE CORTADO Y RARO ASI QUE HAY QUITARLO con solo st.write
    column_scatter1, column_scatter2  = st.columns(2)
    
    with column_scatter1:
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= 0,289 </h6>", unsafe_allow_html=True)    
        
    with column_scatter2:
        st.plotly_chart(fig2, use_container_width=True)
        #st.write(fig2)
    column_scatter3, column_scatter4  = st.columns(2)
    
    with column_scatter3:    
        st.plotly_chart(fig3, use_container_width=True)
        #st.write(fig3)
    with column_scatter4:
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= 0,155 </h6>", unsafe_allow_html=True)

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.markdown("<h5 style='text-align:center; color: white;'> El precio tiene mayor correlación con la longuitud que con la latitud. Cuanto más cerca de la costa se encuentre el inmueble, mayor precio presenta. De igual manera, pero en menor relación, cuanto mas al norte mayor precio también. </h5>", unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    #Scatterplot interactivo de 'minimum_nights' por 'price' de acuerdo al 'room_type'
    st.subheader("Scatterplot interactivo de las variables que mas se relacionan")

    #Scatterplots de variables numericas con mayor correlación
    column1, column2 = st.columns(2)

    with column1:
        #Scatterplot interactivo entre x='reviews_per_month', y='number_of_reviews'
        fig_neighbourhood = px.scatter(df_fil_noches_hc, x='reviews_per_month', y='number_of_reviews', color='neighbourhood', hover_name='neighbourhood')
        st.write(fig_neighbourhood)

        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= 0,913 </h6>", unsafe_allow_html=True)

        #Scatterplot interactivo entre x='calculated_host_listings_count', y='reviews_per_month'
        fig_room_type = px.scatter(df_fil_noches_hc, x='calculated_host_listings_count', y='reviews_per_month', color='room_type', hover_name='room_type')
        st.write(fig_room_type)
        
        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= 0,181 </h6>", unsafe_allow_html=True) 

    with column2:
        #Scatterplot interactivo entre x='availability_365', y='reviews_per_month'    
        fig_room_type = px.scatter(df_fil_noches_hc, x='availability_365', y='reviews_per_month', color='room_type', hover_name='room_type')
        st.write(fig_room_type)

        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= 0,266 </h6>", unsafe_allow_html=True)

        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.markdown("<h5 style='text-align:center; color: white;'> - El número de reviews por mes presenta la mayor correlación entre todas las variables </h5>", unsafe_allow_html=True)
        st.write(" ")
        st.write(" ")
        st.markdown("<h5 style='text-align:center; color: white;'> - Los inmuebles con mayor disponibilidad durante el año presentan mayor número de reviews por mes </h5>", unsafe_allow_html=True)
        st.write(" ")
        st.write(" ")
        st.markdown("<h5 style='text-align:center; color: white;'> - A menor número de anuncios en AirBnB por un anfitrión,  se observó mayor número de reviews por mes</h5>", unsafe_allow_html=True)


    column3, column4 = st.columns(2)

    with column3:
        #Scatterplot interactivo entre x='reviews_per_month', y='minimum_nights' 
        fig_room_type = px.scatter(df_fil_noches_hc, x='reviews_per_month', y='minimum_nights', color='room_type', hover_name='room_type')
        st.write(fig_room_type)

        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= -0,331 </h6>", unsafe_allow_html=True)
        #Scatterplot interactivo entre x='calculated_host_listings_count', y='minimum_nights'
        fig_room_type = px.scatter(df_fil_noches_hc, x='calculated_host_listings_count', y='minimum_nights', color='room_type', hover_name='room_type')
        st.write(fig_room_type)

        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= -0,160</h6>", unsafe_allow_html=True)

    with column4:
        #Scatterplot interactivo entre  x='number_of_reviews', y='minimum_nights'
        fig_room_type = px.scatter(df_fil_noches_hc, x='number_of_reviews', y='minimum_nights', color='room_type', hover_name='room_type')
        st.write(fig_room_type)

        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= -0,278 </h6>", unsafe_allow_html=True)
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.markdown("<h5 style='text-align:center; color: white;'> Relaciones inversas: Los inmuebles que presentan menor número de noches como requisito de alquiler, obtienen mayor número de reviews totales y mensuales; además de mayor número de publicaciones por parte de sus anfitriones en AirBnB. </h5>", unsafe_allow_html=True)
        st.write(" ")
        st.write(" ")
        st.markdown("<h5 style='text-align:center; color: yellow;'> Un número menor mínimo de noches  aumentaría el número de reviews de los inmuebles, lo cual podría influir en el interés de nuevos clientes para la renta de estos inmuebles. </h5>", unsafe_allow_html=True)
        st.write(" ")
        st.write(" ")
        st.markdown("<h5 style='text-align:center; color: yellow;'> El menor número de noches para alquilar un inmueble en Sidney es 1 noche y el número promedio de noches mínimas son 4 noches </h5>", unsafe_allow_html=True)


    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.markdown("<h5 style='text-align: center; color: white;'> Según nos acercamos a la costa el número mínimo de noches aumenta . Los inmuebles con mayor número mínimo de noches tienen mayor precio. </h5>", unsafe_allow_html=True)

    column5, column6 = st.columns(2)

    with column5:
        #Scatterplot interactivo entre  x='longitude', y='minimum_nights'
        fig_room_type = px.scatter(df_fil_noches_hc, x='longitude', y='minimum_nights', color='room_type', hover_name='room_type')
        st.write(fig_room_type)

        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= 0,220 </h6>", unsafe_allow_html=True)
    
    with column6:
        #Scatterplot interactivo entre  x='price', y='minimum_nights'
        fig_room_type = px.scatter(df_fil_noches_hc, x='price', y='minimum_nights', color='room_type', hover_name='room_type')
        st.write(fig_room_type)

        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= 0,197</h6>", unsafe_allow_html=True)
    
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.markdown("<h5 style='text-align: center; color: white;'> A menor número de noches mínimas, mayor disponibilidad de los inmbuebles. Esto influye a que se presenten mayor número de reviews para los inmuebles visitados y se relaciona con que sus anfitriones publiquen más veces en AirBnB </h5>", unsafe_allow_html=True)
    
    column7, column8 = st.columns(2)
    
    with column7:
        #Scatterplot interactivo entre  x='availability_365', y='number_of_reviews'
        fig_room_type = px.scatter(df_fil_noches_hc, x='availability_365', y='number_of_reviews', color='room_type', hover_name='room_type')
        st.write(fig_room_type)

        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= 0,238 </h6>", unsafe_allow_html=True)

    with column8:
        #Scatterplot interactivo entre  x='availability_365', y='calculated_host_listings_count'
        fig_room_type = px.scatter(df_fil_noches_hc, x='availability_365', y='calculated_host_listings_count', color='room_type', hover_name='room_type')
        st.write(fig_room_type)

        st.markdown("<h6 style='text-align: center; color: white;'> (Coeficiente de correlación) r= 0,270 </h6>", unsafe_allow_html=True)




##Concluiones para generar y entrenar un modelo de IAs
with conlusions:
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.markdown("<h1 style='text-align: center; color: white;'> PATRONES DE TENDENCIA Y FUTURAS MEJORAS \n\n </h1>", unsafe_allow_html=True)
    st.write(' ')
    st.write(' ')
    st.markdown("<h3 style='color: yellow;'> -Las variables más correlacionadas de este dataset son: reviews por mes y nº de reviews, entre ellas y con las demás variables. </h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: yellow;'> -A partir de ellas se pueden obtener otros datos interesantes. Ej. Tasa de ocupación </h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: yellow;'> -Mayor número de opiniones generan más interés en las visualizaciones, mayor tasa de rotación. Y por tanto, su relación con el nº mín de noches.", unsafe_allow_html=True)
    st.markdown("<h3 style='color: yellow;'> -Con estos datos se pueden llegar a otro tipo de estudios, como obtener qué nº mín. de noches es más eficiente en términos de rentabilidad según zona geográfica. Relación entre precio medio por noche entre contratos largos y cortos para tomar decisiones según coordenadas o barrios", unsafe_allow_html=True)
    