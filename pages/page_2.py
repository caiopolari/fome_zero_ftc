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
st.set_page_config(page_title = 'Regional', page_icon =':material/south_america:', layout = 'wide')

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

def cuisine_rating_min (df1, cuisine_type):

    """ Esta função tem a responsabilidade de definir qual o nome do restaurante com a menor média de acordo com o tipo de culinária estabelecido
    
    Input:
    - df: Dataframe
    - cuisine_type: Tipo de cozinha
      ex.: 'Italian'
    Output:
    - df: Dataframe """

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

st.header('Plataforma Fome Zero - Regional', divider='rainbow')

with st.sidebar.container():
    #image_path = r"C:\Users\User\Documents\repos\ftc_programacao_python\projeto_aluno\logo.png"
    image = Image.open('logo.png')
    st.sidebar.image(image, width=220)
    st.sidebar.header('Encontre o seu restaurante favorito em qualquer lugar do mundo!')
        
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

restaurant_options = st.sidebar.multiselect('Selecione as características do restaurante:',
                                            ['Faz entrega?', 'Aceita reserva?', 'Aceita pedido online?'])

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

# Filtro das características do restaurante

if 'Faz entrega?' in restaurant_options:
    df1 = df1.loc[df1['is_delivering_now'] == 1, :]

if 'Aceita reserva?' in restaurant_options:
    df1 = df1.loc[df1['has_table_booking'] == 1, :]

if 'Aceita pedido online?' in restaurant_options:
    df1 = df1.loc[df1['has_online_delivery'] == 1, :]

# Filtro do preço médio para duas pessoas em dólares:

linhas_selecionadas = (df1['average_cost_for_two_usd'].between(usd_slider[0], usd_slider[1]))
df1 = df1.loc[linhas_selecionadas, :]

# =======================================
# Layout - Overview
# =======================================

with st.container():
    st.title('Overview')
    col1, col2, col3, col4, col5 = st.columns(5, gap = 'small')
    
    with col1:
        # Exibir o país com mais cidades registradas
        df_aux = df1.loc[:, ['city', 'country_name']].groupby('country_name').nunique().sort_values(by=['city'], ascending = False).reset_index()
        s1 = df_aux['country_name'][0]
        s2 = df_aux['city'].max()
        pais_mais_cidades = "{} - {}".format(s1, s2)
        col1.metric('Cidades registradas', pais_mais_cidades)
        
    with col2:
        # Exibir o país com mais restaurantes registrados
        df_aux = df1.loc[:, ['country_name', 'restaurant']].groupby('country_name').nunique().sort_values(by=['restaurant'], ascending = False).reset_index()
        s1 = df_aux['country_name'][0]
        s2 = df_aux['restaurant'].max()
        pais_mais_restaurantes = "{} - {}".format(s1, s2)
        col2.metric('Restaurantes Registrados', pais_mais_restaurantes)

    with col3:
        # País com a maior quantidade de culinárias diferentes
        df_aux = df1.loc[:, ['country_name', 'cuisines']].groupby(['country_name']).nunique().sort_values(by=['cuisines'], ascending = False).reset_index()
        s1 = df_aux['country_name'][0]
        s2 = df_aux['cuisines'].max()
        pais_mais_culinarias = "{} - {}".format(s1, s2)
        col3.metric('Culinárias diferentes', pais_mais_culinarias)

    with col4:
        # País com a maior quantidade de restaurantes que fazem entregas
        df_aux = df1.loc[:, ['has_online_delivery', 'country_name', 'restaurant']].groupby(['has_online_delivery', 'country_name']).count().reset_index()
        df_aux = df_aux.loc[df_aux['has_online_delivery'] == 1, :].copy().sort_values(by=['restaurant'], ascending = False).reset_index()
        s1 = df_aux['country_name'][0]
        s2 = df_aux['restaurant'].max()
        pais_mais_entregas = "{} - {}".format(s1, s2)
        col4.metric('Fazem entregas', pais_mais_entregas)
        
    with col5:
        # País com a maior quantidade de restaurantes que aceitam reservas
        df_aux = df1.loc[:, ['has_table_booking', 'country_name', 'restaurant']].groupby(['has_table_booking', 'country_name']).count().reset_index()
        df_aux = df_aux.loc[df_aux['has_table_booking'] == 1, :].copy().sort_values(by=['restaurant'], ascending = False).reset_index()
        s1 = df_aux['country_name'][0]
        s2 = df_aux['restaurant'].max()
        pais_mais_reservas = "{} - {}".format(s1, s2)
        col5.metric('Aceitam reservas', pais_mais_reservas)

# =======================================
# Layout - Gráficos
# =======================================

with st.container():
    st.markdown("""---""")
    st.title('Visão Detalhada')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### Avaliação média dos restaurantes por país')
        cols = ['country_name', 'aggregate_rating']
        df_aux = df1.loc[:, cols].groupby(['country_name']).mean().sort_values(by=['aggregate_rating'], ascending = False).reset_index()
        df_aux['aggregate_rating'] = df_aux['aggregate_rating'].round(2)
        df_aux = df_aux.rename(columns = {'country_name': 'País', 'aggregate_rating': 'Avaliação Média'})
        fig = px.bar (df_aux, x = 'País', y = 'Avaliação Média', text_auto = True)
        st.plotly_chart(fig, use_container_width = True)
    with col2:
        st.markdown('##### Custo médio dos restaurantes por país (em USD)')
        cols = ['country_name', 'average_cost_for_two_usd']
        df_aux = df1.loc[:, cols].groupby(['country_name']).mean().sort_values(by=['average_cost_for_two_usd'], ascending = False).reset_index()
        df_aux['average_cost_for_two_usd'] = df_aux['average_cost_for_two_usd'].round(2)
        df_aux = df_aux.rename(columns = {'country_name': 'País', 'average_cost_for_two_usd': 'Preço Médio para Dois (USD)'})
        fig = px.bar (df_aux, x = 'País', y = 'Preço Médio para Dois (USD)', text_auto = True)
        st.plotly_chart(fig, use_container_width = True)
with st.container():
    st.markdown('##### 10 Cidades com mais restaurantes registrados')
    cols = ['city', 'restaurant_name', 'country_name']
    df_aux = df1.loc[:, cols].groupby(['city', 'country_name']).nunique().sort_values(by=['restaurant_name'], ascending = False).reset_index()
    df_aux = df_aux.rename(columns = {'city': 'Cidade', 'restaurant_name': 'Número de Restaurantes', 'country_name': 'País'})
    fig = px.bar (df_aux.head(10), x = 'Cidade', y = 'Número de Restaurantes', color = 'País', text_auto = True)
    st.plotly_chart(fig, use_container_width = True)

with st.container():
    st.markdown("""---""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### 10 Cidades com maior valor médio do prato para duas pessoas (em USD)')
        cols = ['city', 'average_cost_for_two_usd', 'country_name']
        df_aux = df1.loc[:, cols].groupby(['city', 'country_name']).mean().sort_values(by=['average_cost_for_two_usd'], ascending = False).reset_index()
        df_aux['average_cost_for_two_usd'] = df_aux['average_cost_for_two_usd'].round(2)
        df_aux = df_aux.rename(columns = {'city': 'Cidade', 'average_cost_for_two_usd': 'Preço Médio para Dois (USD)', 'country_name': 'País'})
        fig = px.bar (df_aux.head(10), x = 'Cidade', y = 'Preço Médio para Dois (USD)', color = 'País', text_auto = True)
        st.plotly_chart(fig, use_container_width = True)

    with col2:
        st.markdown('##### 10 Cidades com mais variedades de culinárias')
        cols = ['city', 'cuisines', 'country_name']
        df_aux = df1.loc[:, cols].groupby(['city', 'country_name']).count().sort_values(by=['cuisines'], ascending = False).reset_index()
        df_aux = df_aux.rename(columns = {'city': 'Cidade', 'cuisines': 'Tipos de Culinária', 'country_name': 'País'})
        fig = px.bar (df_aux.head(10), x = 'Cidade', y = 'Tipos de Culinária', color = 'País', text_auto = True)
        st.plotly_chart(fig, use_container_width = True)