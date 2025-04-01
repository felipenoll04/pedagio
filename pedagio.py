import random
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
cursor.execute("DELETE FROM ticket")
cursor.execute("SELECT id_pista FROM pista")
pistas = cursor.fetchall()
cursor.execute("SELECT id_praca_pedagio FROM praca_pedagio")
pedagios = cursor.fetchall()
cursor.execute("SELECT id_funcionario FROM funcionario")
funcionarios = cursor.fetchall()
cursor.execute("SELECT id_veiculo FROM veiculo")
veiculos = cursor.fetchall()
cursor.execute("SELECT id_valor_tipo_veiculo FROM valor_tipo_veiculo")
valores_tipo_veiculo = cursor.fetchall()

# Função para inserir tickets em lotes para não crashar
def inserir_tickets(qtd):
    batch_size = 10000
    for i in range(1, qtd + 1, batch_size):
        tickets = [
            (j, fake.date_between(start_date="-1y"), random.choice(pistas)[0], random.choice(pedagios)[0],
             random.choice(funcionarios)[0], random.choice(veiculos)[0], random.choice(valores_tipo_veiculo)[0])
            for j in range(i, min(i + batch_size, qtd + 1))
        ]
        cursor.executemany("INSERT INTO ticket (id_ticket, data, id_pista, id_praca_pedagio, id_funcionario, id_veiculo, id_valor_tipo_veiculo) VALUES (%s, %s, %s, %s, %s, %s, %s)", tickets)
        conn.commit()

# Inserts dos tickets
inserir_tickets(1000000)
#inserir_tickets(10000000)
#inserir_tickets(100000000)
cursor.close()
conn.close()