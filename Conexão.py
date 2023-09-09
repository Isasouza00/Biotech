# IMPORTANDO BIBLIOTECAS
import mysql.connector

# CONECTANDO AO DB
conexao = mysql.connector.connect(host='localhost', user='root',
                                  password='admin', database='biotechdb')

# CRIANDO CURSOR
cursor = conexao.cursor()

# INSERINDO DADOS USUÁRIO
def inserir_usuario(nome, cpf, email, senha):
    comando = f'INSERT INTO tb_usuario (nome, cpf, email, senha) VALUES ("{nome}", "{cpf}", "{email}", "{senha}")'
    cursor.execute(comando)
    conexao.commit()
