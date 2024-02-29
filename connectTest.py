from sqlalchemy import create_engine

# Substitua o IP abaixo pelo IP correto do seu Docker host
# Substitua a senha e outros detalhes conforme necessário

db_name = 'test_db'
db_user = 'root'
db_pass = '12345'
db_host = 'db'
db_port = '5432'
db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
print(db_url)
# Imprimir a string de conexão em hexadecimais
print("String de Conexão (Hex):", db_url.encode('utf-8').hex())

try:
    # Tentar criar a engine
    engine = create_engine(db_url)

    # Tentar estabelecer uma conexão
    connection = engine.connect()
    print("Conexão bem-sucedida!")

    # Fechar a conexão
    connection.close()

except Exception as e:
    # Imprimir informações de rastreamento
    import traceback
    traceback.print_exc()

    print(f"Erro de conexão: {e}")
