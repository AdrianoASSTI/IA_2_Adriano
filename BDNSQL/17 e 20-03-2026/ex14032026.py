import pandas as pd
from pymongo import MongoClient

def conectar_mongodb():
    # Substitua pela sua string de conexão se estiver usando o Atlas
    client = MongoClient("mongodb://localhost:27017/")
    
    # Selecionando o banco e a coleção
    db = client["local"]
    collection = db["ex14-03-26"]
    
    # Buscando os dados no MongoDB
    # O find() retorna um cursor, transformamos em lista para o Pandas
    dados = list(collection.find())
    
    # Criando o DataFrame
    df = pd.DataFrame(dados)
    
    # Removendo a coluna '_id' do MongoDB para visualização mais limpa, se desejar
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])
    
    return df

if __name__ == "__main__":
    try:
        df_mongo = conectar_mongodb()
        
        print("--- Conexão realizada com sucesso! ---")
        print(f"Total de registros encontrados: {len(df_mongo)}")
        
        print("\n--- Exibindo as 5 primeiras amostras (Pandas) ---")
        print(df_mongo.head(5))
        
    except Exception as e:
        print(f"Erro ao conectar ou processar dados: {e}")