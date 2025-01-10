import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Carregar o arquivo XLSX e preparar os dados
df = pd.read_excel("C:\\Users\\fyogi\\Downloads\\rotas-rurais\\Reclass\\DB_ReclassKernel_rec_NOME_BUSCA_Operados.xlsx")

# Converte a coluna 'Area' para Km², se necessário (assumindo que está em metros quadrados)
if df['Area'].max() > 1000000:  # A área provavelmente está em metros quadrados
    df['Area'] = df['Area'] / 1_000_000  # Converte metros quadrados para Km²

# Título da página
st.title("Distribuição de Áreas por Município e Classe DN")

# Lista suspensa para selecionar o município
municipio_selecionado = st.selectbox(
    'Selecione o Município',
    options=df['MUN'].unique(),
    index=0  # Valor inicial do dropdown
)

# Filtra os dados para o município selecionado
df_filtrado = df[df['MUN'] == municipio_selecionado]

# Agrupa os dados por classe 'DN' e soma as áreas
soma_areas = df_filtrado.groupby('DN')['Area'].sum()

# Cria o gráfico de pizza com Plotly
fig = go.Figure(data=[go.Pie(labels=soma_areas.index, values=soma_areas, hole=0.3)])
fig.update_layout(title=f'Distribuição de Áreas por Classe DN - {municipio_selecionado}', title_x=0.5)

# Exibe o gráfico
st.plotly_chart(fig)

# Exibe as áreas por classe como uma lista
st.subheader("Áreas por Classe DN")
for dn_class, area in soma_areas.items():
    st.write(f'Classe {dn_class}: {area:.2f} km²')

