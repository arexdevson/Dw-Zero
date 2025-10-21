# imports
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#imports das variaveis de ambiente

load_dotenv()


DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

#dados commodities

commodities = ['CL=F','GC=F','SI=F']

"""
5d = 5 dias
5m = 5 meses
5y = 5 anos...
"""
def buscar_dados_commodities(simbolo,periodo='5d',intervalo='1d'):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo,interval=intervalo)[['Close']]
    dados['simbolo'] = simbolo
    return dados

def buscar_todos_dados_commodities(commodities):
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)


def salvar_no_postgres(df,schema='public'):
    df.to_sql('commodities',engine,if_exists='replace',index=True,index_label='Date',schema=schema)


# concatenar os ativos

if __name__ == "__main__":
    dados_concatenatados = buscar_todos_dados_commodities(commodities) #pegar cotação dos ativos
    salvar_no_postgres(dados_concatenatados)

# salvar no banco de dados

"""

-- remover readme
git rm README.md

-- criar readme
echo "# Titulo do Projeto" > README.md

-- descrição do readme
echo "Descricao do projeto..." >> README.md

git commit -m "Refeito o arquivo README.md"

git push -u origin main 

-- Mensagem no readme, não precisa = echo "# Dw-Zero" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/arexdevson/Dw-Zero.git
git push -u origin main

----- outro exemplo de gitada

git add .
git commit -m "feat: adicionar feature de extract e load - task: xxxx"
git push


limpartela do terminal
clear

ambiente virtual = organizar versionamente do projeto = python -m venv .venv
.venv/Scripts/activate

pip install -r requirements.txt


AWS - POSTGRESSQL (PÕE CARTÃO)

ACESSO A CONTA FREE TIER DA AWS
VOU NA BARRA DE BUSCA POR RDS (RELATIONAL DATABASES)
DASHBOARD - PAINEL E CRIO UM BANCO DE DADOS POSTGRES
** MUITA ATENÇAO NO QUE ESCOLHER PRA NÃO PAGAR!!!

DAR NOME PRO BANCO
USUARIO
SENHA
PUBLICO OU PRIVADO?
E CRIO

"""
