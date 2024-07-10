# Libraries
import pandas as pd
import inflection
import folium
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from haversine import haversine
from PIL import Image
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Configurando a página
st.set_page_config(page_title = 'Main Page', page_icon =':material/analytics:', layout = 'wide')

# =======================================
# Funções
# =======================================

def cuisine_rating_max (df1, cuisine_type):

    """ Esta função tem a responsabilidade de definir qual o nome do restaurante com a maior média de acordo com o tipo de culinária estabelecido
    
    Input:
    - df: Dataframe
    - cuisine_type: Tipo de cozinha
      ex.: 'Italian'
    Output:
    - df: Dataframe """

    cols = ['cuisines', 'aggregate_rating', 'restaurant_name', 'country_name', 'city', 'average_cost_for_two_usd']

    df_aux = df1.loc[:, cols].groupby(['restaurant_name', 'cuisines', 'aggregate_rating', 'country_name', 'city', 'average_cost_for_two_usd']).mean().reset_index()

    linhas_selecionadas = (df_aux['cuisines'] == cuisine_type)
    df_aux = df_aux.loc[linhas_selecionadas, :].max().copy().reset_index()

    return (df_aux)

    """ Esta função tem a responsabilidade de definir qual o nome do restaurante com a menor média de acordo com o tipo de culinária estabelecido
    
    Input:
    - df: Dataframe
    - cuisine_type: Tipo de cozinha
      ex.: 'Italian'
    Output:
    - df: Dataframe """

def cuisine_rating_min (df1, cuisine_type):

    cols = ['cuisines', 'aggregate_rating', 'restaurant_name']
    
    df_aux = df1.loc[:, cols].groupby(['restaurant_name', 'cuisines', 'aggregate_rating']).mean().reset_index()
    
    linhas_selecionadas = (df_aux['cuisines'] == cuisine_type)
    df_aux = df_aux.loc[linhas_selecionadas, :].min().copy().reset_index()

    return (df_aux)

to_USD = {
    'Indonesia': 0.000061,
    'Australia': 0.67,
    'Sri Lanka': 0.0033,
    'Philippines': 0.017,
    'India': 0.012,
    'South Africa': 0.056,
    'Qatar': 0.27,
    'United Arab Emirates': 0.27,
    'Singapure': 0.74,
    'Brazil': 0.18,
    'Turkey': 0.03,
    'New Zeland': 0.61,
    'United States of America': 1,
    'England': 1.26,
    'Canada': 0.73,
}
def convert_to_usd(country_name):
    
    """ Esta função tem a responsabilidade de definir o critério de conversão da moeda local para USD
    
    Input: Nome do país 'country_name'
    Output: Fator de conversão para USD"""

    return to_USD(country_name)

    """ Esta função tem a responsabilidade de categorizar o ID de cada país e substituir pelo seu respectivo nome
    
    Input: ID situada na coluna 'country_ID'
    Saída: Nome do respectivo país """

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

def create_price_type(price_range):
    
    """ Esta função tem a responsabilidade de categorizar os números da coluna price_range em uma string com o preço
    
    Input: Preço na coluna price_range
    Output: Categorização de preço """
    
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    
    """ Esta função tem a responsabilidade de assignar cada código de cor em um nome
    
    Input: Código de cor na coluna color_code
    Output: Descrição da cor"""
    
    return COLORS[color_code]

def rename_columns(dataframe):

    """ Esta função tem como responsabilidade renomear todas as colunas do data frame
    
    Input: Dataframe
    Output: Dataframe """
    
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def clean_code(df):
    df = rename_columns(df)
    df['color_code'] = df['rating_color'].map(COLORS)
    df['country_name'] = df['country_code'].map(COUNTRIES)
    df['price_range_description'] = df['price_range'].apply(create_price_type)
    df['to_usd_factor'] = df['country_name'].map(to_USD)
    
    # Limpeza de dados
    
    df = df.loc[df['cuisines'] != 'nan', :].copy()
    df = df.loc[df['is_delivering_now'] != 'NaN', :].copy()
    df = df.loc[df['has_online_delivery'] != 'NaN', :].copy()
    df = df.loc[df['has_table_booking'] != 'NaN', :].copy()
    df = df.loc[df['average_cost_for_two'] < 25000016, :].copy()
    df = df.loc[df['cuisines'] != 'nan', :].copy()
    df = df.loc[df['cuisines'] != 'Mineira ', :].copy()
    df = df.loc[df['cuisines'] != 'Drinks Only', :].copy()
    
    # Convertendo a coluna de custo médio para cada duas pessoas para dólar
    
    df['average_cost_for_two_usd'] = df['average_cost_for_two'] * df['to_usd_factor']

    return (df)

# =======================================
# Import e Limpeza de Dados
# =======================================

# Import dataset
df = pd.read_csv('dataset/zomato.csv')

# Limpando dataset
df1 = clean_code(df)

# Renomeando colunas
df1 = rename_columns(df1)

# Categorizar restaurantes por apenas um tipo de culinária

df1['cuisines'] = df1.loc[:, 'cuisines'].astype(str).apply(lambda x: x.split(",")[0])

## Regional

# =======================================
# Barra lateral
# =======================================

st.header('Plataforma Fome Zero - Main Page', divider='rainbow')

with st.sidebar.container():
    #image_path = r"C:\Users\User\Documents\repos\ftc_programacao_python\projeto_aluno\logo.png"
    image = Image.open('logo.png')
    st.sidebar.image(image, width=220)
        
st.sidebar.markdown ("""---""")

container = st.sidebar.container()
all = st.sidebar.checkbox("Selecione todos os países", value=True)
 
if all:
    country_options = st.sidebar.multiselect("Selecione os países desejados:",
         ['India','United States of America','Philippines','South Africa', 'England', 'New Zeland', 'United Arab Emirates', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'Turkey', 'Qatar', 'Singapure', 'Sri Lanka'],['India','United States of America','Philippines','South Africa', 'England', 'New Zeland', 'United Arab Emirates', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'Turkey', 'Qatar', 'Singapure', 'Sri Lanka'])
else:
    country_options =  st.sidebar.multiselect("Selecione um ou mais países:",
        ['India','United States of America','Philippines','South Africa', 'England', 'New Zeland', 'United Arab Emirates', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'Turkey', 'Qatar', 'Singapure', 'Sri Lanka'])

st.sidebar.markdown ("""---""")

rating_slider = st.sidebar.slider('Selecione as notas desejadas:', 
                                  min_value = 0.0, 
                                  max_value = 5.0, 
                                  value = (0.0, 5.0))

st.sidebar.markdown ("""---""")

usd_slider = st.sidebar.slider('Selecione o preço médio para duas pessoas (em USD):', 
                               min_value = df1['average_cost_for_two_usd'].min(), 
                               max_value = df1['average_cost_for_two_usd'].max(), 
                               value = (df1['average_cost_for_two_usd'].min(), 
                                        df1['average_cost_for_two_usd'].max()))

st.sidebar.markdown ("""---""")
st.sidebar.markdown ('##### Desenvolvido por')
st.sidebar.markdown ('##### Caio Polari de Souza')
st.sidebar.markdown ('##### @caiopolari')

# Filtro de notas

linhas_selecionadas = (df1['aggregate_rating'].between(rating_slider[0], rating_slider[1]))
df1 = df1.loc[linhas_selecionadas, :]

# Filtro do nome do país

linhas_selecionadas = (df1['country_name'].isin(country_options))
df1 = df1.loc[linhas_selecionadas, :]

# Filtro do preço médio para duas pessoas em dólares:

linhas_selecionadas = (df1['average_cost_for_two_usd'].between(usd_slider[0], usd_slider[1]))
df1 = df1.loc[linhas_selecionadas, :]

# =======================================
# Layout Central
# =======================================

st.header('Encontre o seu restaurante favorito em qualquer lugar do mundo!')

st.markdown ("""---""")

with st.container():
    st.title('Visão Geral da Plataforma')
    col1, col2, col3, col4, col5 = st.columns(5, gap = 'small')
    
    with col1:
        # Exibir o total de países cadastrados
        paises_cadastrados = df1.loc[:, ['country_name']].nunique()
        col1.metric('Países cadastrados', paises_cadastrados)
        
    with col2:
        # Exibir o total de cidades cadastradas
        cidades_cadastradas = df1.loc[:, ['city']].nunique()
        col2.metric('Cidades Cadastradas', cidades_cadastradas)

    with col3:
        # Exibir o total de restaurantes cadastrados
        restaurantes_cadastrados = df1.loc[:, ['restaurant']].nunique()
        col3.metric('Restaurantes Cadastradas', restaurantes_cadastrados)

    with col4:
        # Exibir o total de avaliações feitas
        avaliacoes_feitas = df1['votes'].sum()
        col4.metric('Avaliações Feitas', '{0:,}'.format(avaliacoes_feitas))
        
    with col5:
        # Exibir o número de culinárias
        culinarias_cadastradas = df1.loc[:, ['cuisines']].nunique()
        col5.metric('Culinárias Cadastradas', culinarias_cadastradas)

st.markdown ("""---""")

with st.container():
    df_aux = df1.loc[:, ['latitude', 'longitude', 'restaurant_name', 'average_cost_for_two', 'currency', 'cuisines', 'aggregate_rating', 'rating_color']]
    map=folium.Map(location=[df_aux['latitude'].mean(), df_aux['longitude'].mean()], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(map)
    for index, location_info in df_aux.iterrows():
        popup_text = ('<h3><b>' + location_info['restaurant_name'] + '</b></h3>' + '<br>' + 
                      '<b>Price: </b>' + f'{location_info['average_cost_for_two']}' + ' ' + '(' + location_info['currency'] + ')' + ' para dois' + '<br>' + 
                      '<b>Type: </b>' + location_info['cuisines'] + '<br>' + 
                      '<b>Aggregate Rating: </b>' + f'{location_info['aggregate_rating']}' + '/5.0')

        folium.Marker([location_info['latitude'], 
                       location_info['longitude']], 
                       popup=folium.Popup(popup_text,
                                           max_width=300), 
                       icon=folium.Icon(color=location_info['rating_color'], 
                                        icon='home')).add_to(marker_cluster)

folium_static(map, width=1024, height=600)