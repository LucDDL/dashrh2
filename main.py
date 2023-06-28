import streamlit as st
import pandas as pd
import os
import json

# Função para salvar os dados em um arquivo JSON local
def salvar_dados_localmente(data):
    # Criação do diretório se não existir
    if not os.path.exists("dados"):
        os.makedirs("dados")

    # Caminho do arquivo JSON
    file_path = os.path.join("dados", "dados.json")

    # Salvando os dados no arquivo JSON
    with open(file_path, "w") as file:
        json.dump(data, file)


def carregar_dados_localmente():
    # Caminho do arquivo JSON
    file_path = os.path.join("dados", "dados.json")

    # Verifica se o arquivo JSON existe
    if os.path.exists(file_path):
        # Carrega os dados do arquivo JSON
        with open(file_path, "r") as file:
            data = json.load(file)
            return data

    return None


# Configuração do sidebar
st.sidebar.title("DASHBOARD - RH")
pages = ["ANALITICO", "CARGA"]
selected_page = st.sidebar.selectbox("Página", pages)

# Colunas que você deseja selecionar
colunas_selecionadas = [
    "nome_evento",
    "data_inicio_do_evento",
    "data_fim_do_evento",
    "uf",
    "tipo_evento",
    "tipo_de_produto",
    "status",
    "qtd_totem",
    "qtd_smartpos",
    "qtd_pdv",
    "publico_estimado_por_dia",
]

valores_tipo_evento = ['Evento', 'Outros', 'Feira', 'Festival']

# Página "ANALITICO"
if selected_page == "ANALITICO":
    # Carrega os dados do arquivo JSON local ou cria um DataFrame vazio
    data = carregar_dados_localmente() or []

    # Exibe o DataFrame
    df = pd.DataFrame(data)
    df = df[colunas_selecionadas].copy()  # selecionar apenas as colunas desejadas

    # Adicionar nova coluna 'total_de_maquinas'
    df['total_de_maquinas'] = ((df['qtd_totem'].fillna(0) + df['qtd_smartpos'].fillna(0) + df['qtd_pdv'].fillna(0)) / 60)
    df.loc[df['total_de_maquinas'] != 0, 'total_de_maquinas'] = df['total_de_maquinas'].astype(int)

    # Filtrar pela coluna "tipo_evento"
    df = df[(df["tipo_evento"].isin(valores_tipo_evento)) | (df["tipo_evento"].isnull())]

    # Sidebar - Selecionar status
    status = df["status"].dropna().unique().tolist()
    status.insert(0, "Todos")
    selected_status = st.sidebar.selectbox("Status", status)

    if selected_status != "Todos":
        df = df[df["status"] == selected_status]

    st.dataframe(df)

# Página "CARGA"
elif selected_page == "CARGA":
    # Título da página
    st.title("Upload de Arquivo JSON")

    # Upload do arquivo JSON
    uploaded_file = st.file_uploader("Selecione um arquivo JSON", type="json")

    if uploaded_file is not None:
        # Leitura do arquivo JSON
        data = json.load(uploaded_file)
        salvar_dados_localmente(data)

        # Exibe o DataFrame
        st.subheader("DataFrame do arquivo JSON:")
        df = pd.DataFrame(data)
        df = df[colunas_selecionadas].copy()  # selecionar apenas as colunas desejadas

        # Adicionar nova coluna 'total_de_maquinas'
        df['total_de_maquinas'] = ((df['qtd_totem'].fillna(0) + df['qtd_smartpos'].fillna(0) + df['qtd_pdv'].fillna(0)) / 60)
        df.loc[df['total_de_maquinas'] != 0, 'total_de_maquinas'] = df['total_de_maquinas'].astype(int)

        st.dataframe(df)

        # Mensagem de sucesso
        st.success("Os dados foram carregados com sucesso.")
