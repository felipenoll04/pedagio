import random
import pandas as pd
import psycopg2
from faker import Faker

# Conexão com o banco
conn = psycopg2.connect(
    dbname="pedagio",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

fake = Faker()

# Selecionar os ids das tabelas
cursor.execute("SELECT id_pista FROM pista")
pistas = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT id_praca_pedagio FROM praca_pedagio")
pedagios = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT id_funcionario FROM funcionario")
funcionarios = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT id_veiculo FROM veiculo")
veiculos = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT id_valor_tipo_veiculo FROM valor_tipo_veiculo")
valores_tipo_veiculo = [row[0] for row in cursor.fetchall()]

cursor.close()
conn.close()

# Função para gerar os tickets
def gerar_tickets(qtd):
    tickets = [{
        "id_ticket": i,
        "data": fake.date_between(start_date="-1y"),
        "id_pista": random.choice(pistas),
        "id_praca_pedagio": random.choice(pedagios),
        "id_funcionario": random.choice(funcionarios),
        "id_veiculo": random.choice(veiculos),
        "id_valor_tipo_veiculo": random.choice(valores_tipo_veiculo)
    } for i in range(1, qtd + 1)]

    df = pd.DataFrame(tickets)
    df.to_csv('tickets.csv', index=False)


# Inserts dos tickets
gerar_tickets(1000000)
#gerar_tickets(10000000)
#gerar_tickets(100000000)