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
st.set_page_config(page_title = 'Minimalista', page_icon =':material/restaurant:', layout = 'wide')

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

st.header('Plataforma Fome Zero - Minimalista', divider='rainbow')

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

container = st.sidebar.container()
all = st.sidebar.checkbox("Selecione todas as culinárias", value=True)
cuisine = ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
       'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
       'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
       'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
       'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
       'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
       'Continental', 'South Indian', 'North Indian', 'Salad',
       'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
       'South African', 'Drinks Only', 'Durban', 'World Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
       'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
       'Kokoreç']
if all:
    cuisine_options = st.sidebar.multiselect("Selecione as culinárias desejadas:", cuisine, cuisine)
else:
    cuisine_options =  st.sidebar.multiselect("Selecione as culinárias desejadas:", cuisine)

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

# Filtro das culinárias

df1 = df1.loc[df1['cuisines'].isin(cuisine_options), :]

# Filtro do preço médio para duas pessoas em dólares:

linhas_selecionadas = (df1['average_cost_for_two_usd'].between(usd_slider[0], usd_slider[1]))
df1 = df1.loc[linhas_selecionadas, :]

# =======================================
# Layout Central
# =======================================

with st.container():
    st.title('Melhores Restaurantes')
    col1, col2, col3, col4, col5 = st.columns(5, gap = 'small')
    with col1:
        american = cuisine_rating_max (df1, 'American')
        st.write('#### American')
        st.markdown(american.iloc[0, 1])
        st.markdown(f'## {american.iloc[2, 1]}/5.0')
        st.info(f'Country: {american.iloc[3, 1]}', icon=":material/map:")
        st.info(f'City: {american.iloc[4, 1]}', icon=":material/location_on:")
        st.info(f'Average Cost for Two: ${american.iloc[5, 1]}',icon=":material/paid:")
    with col2:
        japanese = cuisine_rating_max (df1, 'Japanese')
        st.write('#### Japanese')
        st.markdown(japanese.iloc[0, 1])
        st.markdown(f'## {japanese.iloc[2, 1]}/5.0')
        st.info(f'Country: {japanese.iloc[3, 1]}', icon=":material/map:")
        st.info(f'City: {japanese.iloc[4, 1]}', icon=":material/location_on:")
        st.info(f'Average Cost for Two: ${japanese.iloc[5, 1]}',icon=":material/paid:")
    with col3:
        italian = cuisine_rating_max (df1, 'Italian')
        st.write('#### Italian')
        st.markdown(italian.iloc[0, 1])
        st.markdown(f'## {italian.iloc[2, 1]}/5.0')
        st.info(f'Country: {italian.iloc[3, 1]}', icon=":material/map:")
        st.info(f'City: {italian.iloc[4, 1]}', icon=":material/location_on:")
        st.info(f'Average Cost for Two: ${italian.iloc[5, 1]}',icon=":material/paid:")
    with col4:
        arabian = cuisine_rating_max (df1, 'Arabian')
        st.write('#### Arabian')
        st.markdown(arabian.iloc[0, 1])
        st.markdown(f'## {arabian.iloc[2, 1]}/5.0')
        st.info(f'Country: {arabian.iloc[3, 1]}', icon=":material/map:")
        st.info(f'City: {arabian.iloc[4, 1]}', icon=":material/location_on:")
        st.info(f'Average Cost for Two: ${arabian.iloc[5, 1].round(2)}',icon=":material/paid:")
    with col5:
        homemade = cuisine_rating_max (df1, 'Home-made')
        st.write('#### Home-made')
        st.markdown(homemade.iloc[0, 1])
        st.markdown(f'## {homemade.iloc[2, 1]}/5.0')
        st.info(f'Country: {homemade.iloc[3, 1]}', icon=":material/map:")
        st.info(f'City: {homemade.iloc[4, 1]}', icon=":material/location_on:")
        st.info(f'Average Cost for Two: ${homemade.iloc[5, 1]}',icon=":material/paid:")

with st.container():
    st.markdown("""---""")
    st.subheader("Customize a sua pesquisa de culinária")
    custom_option = st.selectbox("Selecione a culinária desejada", cuisine)
    custom = cuisine_rating_max (df1, custom_option)
    st.write(f'#### {custom_option}')
    st.markdown(custom.iloc[0, 1])
    st.markdown(f'## {custom.iloc[2, 1]}/5.0')
    st.info(f'Country: {custom.iloc[3, 1]}', icon=":material/map:")
    st.info(f'City: {custom.iloc[4, 1]}', icon=":material/location_on:")
    st.info(f'Average Cost for Two: ${custom.iloc[5, 1]}',icon=":material/paid:")

with st.container():
    st.markdown("""---""")
    st.markdown('## Os Melhores Restaurantes com as Principais Culinárias')
    col1, col2 = st.columns(2, gap = 'small')
    with col1:
        st.markdown('##### Top 10 culinárias mais bem avaliadas')
        cols = ['cuisines', 'aggregate_rating']
        df_aux = df1.loc[:, cols].groupby(['cuisines']).mean().sort_values(by='aggregate_rating', ascending = False).round(2).reset_index()
        df_aux = df_aux.rename(columns = {'cuisines': 'Culinárias', 'aggregate_rating': 'Avaliação Média'})
        fig = px.bar(df_aux.head(10), y = 'Avaliação Média', x = 'Culinárias', text_auto = True)
        st.plotly_chart(fig, use_container_width = True)
    with col2:
        st.markdown('##### Top 10 culinárias mais bem avaliadas')
        cols = ['cuisines', 'aggregate_rating']
        df_aux = df1.loc[:, cols].groupby(['cuisines']).mean().sort_values(by='aggregate_rating', ascending = True).round(2).reset_index()
        df_aux = df_aux.rename(columns = {'cuisines': 'Culinárias', 'aggregate_rating': 'Avaliação Média'})
        fig = px.bar(df_aux.iloc[2:12], y = 'Avaliação Média', x = 'Culinárias', text_auto = True)
        st.plotly_chart(fig, use_container_width = True)
    