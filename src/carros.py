import pyodbc
import streamlit as st

# Função para conectar ao banco de dados com tratamento de exceções
@st.cache(allow_output_mutation=True)
def connect_to_db():
    try:
        server = st.secrets["server"]
        database = st.secrets["database"]
        username = st.secrets["username"]
        password = st.secrets["password"]
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        return pyodbc.connect(connection_string)
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para inserir um novo registro na tabela com tratamento de exceções
def insert_into_table(tipo, marca, modelo, cor, combustivel, ano, preco):
    try:
        conn = connect_to_db()
        if conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO STG.CadastroVeiculos (Tipo, Marca, Modelo, Cor, Combustivel, Ano, Preco)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query, (tipo, marca, modelo, cor, combustivel, ano, preco))
                conn.commit()
            st.success('Dados inseridos com sucesso!')
    except Exception as e:
        st.error(f"Erro ao inserir dados: {e}")
    finally:
        if conn:
            conn.close()

# Interface gráfica com Streamlit
st.title('Cadastro de Veículos da Chronos Car')

# Opções para os campos
tipos = ['Carro', 'Moto', 'Caminhão']

marcas = [  'Volkswagen', 'Toyota', 'Hyundai', 'Fiat', 
            'Ford', 'Honda', 'Chevrolet', 'Renault', 
            'BMW', 'Mercedes-Benz', 'Nissan', 'Peugeot', 
            'Audi', 'Kia', 'Land Rover', 'Mitsubishi', 
            'JAC', 'GWM', 'BYD', 'RAM']

cores = [   'Preto', 'Branco', 'Vermelho', 'Prata',
            'Azul', 'Verde', 'Laranja', 'Bege',]

combustiveis = ['Gasolina', 'Diesel', 'Elétrico', 'Flex']

modelos_por_marca = {
    'Volkswagen': ['Gol', 'Polo', 'T-Cross', 'Taos', 'Amarok', 'Nivus', 'Jetta'],
    'Toyota': ['Corolla', 'Corolla Cross', 'Etios', 'Hilux', 'RAV4', 'SW4'],
    'Hyundai': ['Gol', 'Polo', 'T-Cross', 'Taos', 'Amarok', 'Nivus', 'Jetta'],
    'Fiat': ['Mobi', 'Argo', 'Cronos', 'Pulse', 'Fastback', 'Uno', 'Palio', 'Siena', 'Ducato', 'Strada', 'Toro'],
    'Ford': ['EcoSport', 'Fiesta', 'Fusion', 'Ka Hatch', 'Ka Sedan', 'Mustang', 'Ranger'],
    'Honda': ['Accord', 'City', 'Civic', 'CR-V', 'Fit', 'HR-V', 'WR-V'],
}

# Campos para inserção de dados com opções
tipo = st.selectbox('Tipo', tipos)
marca = st.selectbox('Marca', marcas)
modelos = modelos_por_marca.get(marca, [])
modelo = st.selectbox('Modelo', modelos)
cor = st.selectbox('Cor', cores)
combustivel = st.selectbox('Combustível', combustiveis)
ano = st.number_input('Ano', step=1, format="%d")
preco = st.number_input('Preço', step=0.01, format="%.2f")

# Botão para inserir os dados
if st.button('Inserir Registro'):
    insert_into_table(tipo, marca, modelo, cor, combustivel, ano, preco)
    st.success('Dados inseridos com sucesso!')