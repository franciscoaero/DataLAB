import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2

def buscaSite(url, filename):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content_modules = soup.find_all('div', class_='contentModule')

        data = []

        for i, content_module in enumerate(content_modules, 1):
            semestre = content_module.find('h3').text.strip()
            modulos = content_module.find_all('h4')

            for modulo in modulos:
                titulo_modulo = modulo.text.strip()

                # Encontrar todas as descrições e cargas horárias dentro do módulo
                descricoes = modulo.find_next('ul').find_all('li')

                for descricao in descricoes:
                    disciplina = descricao.text.strip().replace('HORAS', '')
                    carga_horaria = disciplina.split()[-1] + ' H'
                    disciplina = ' '.join(disciplina.split()[:-1])

                    # Tentar forçar a codificação para UTF-8
                    encoded_disciplina = disciplina.encode('utf-8', 'ignore').decode('utf-8')
                    encoded_row = [semestre, titulo_modulo, encoded_disciplina, carga_horaria]

                    data.append(encoded_row)

        try:
            # Conectar ao banco de dados PostgreSQL
            connection = psycopg2.connect(
                user="postgres",
                password="12345",
                host="localhost",
                port="5432",
                database="postgres",
                options="-c client_encoding=utf-8"
            )

            print("Conexão bem-sucedida!")

            # Criar um cursor para executar comandos SQL (com a codificação utf-8)
            cursor = connection.cursor(encoding='utf-8')

            # Criar a tabela se ela não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cursos (
                    semestre VARCHAR(255),
                    titulo_modulo VARCHAR(255),
                    disciplina VARCHAR(255),
                    carga_horaria VARCHAR(10)
                ) WITH (ENCODING='UTF8')
            """)

            # Inserir dados na tabela
            for row in data:
                # Usar cursor.mogrify para lidar com a codificação
                mogrified_row = cursor.mogrify("""
                    INSERT INTO cursos (semestre, titulo_modulo, disciplina, carga_horaria)
                    VALUES (%s, %s, %s, %s)
                """, row)

                cursor.execute(mogrified_row)

            # Commit as alterações e fechar a conexão
            connection.commit()
            connection.close()
            print("Dados inseridos com sucesso!")

        except psycopg2.Error as e:
            print(f"Erro ao conectar/inserir dados no banco: {e}")

    else:
        print(f"Erro na requisição. Código de status: {response.status_code}")

# Chama a função com o URL e nome do arquivo desejado
buscaSite("https://ead.unisagrado.edu.br/cursos-graduacao/engenharia-de-software-ead?", "EngenhariaSoftware")
