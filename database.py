# IMPORTANDO BIBLIOTECAS
import mysql.connector

# CONECTANDO AO DB BIOTECH
conexao = mysql.connector.connect(host='localhost', user='root',
                                  password='admin', database='biotechdb')

# CRIANDO CURSOR
cursor = conexao.cursor()

# INSERINDO DADOS USUÁRIO
def inserir_usuario(nome, cpf, email, senha):
    comando = f'INSERT INTO tb_usuarios (nome, cpf, email, senha) VALUES ("{nome}", "{cpf}", "{email}", "{senha}")'
    cursor.execute(comando)
    conexao.commit()

#VER EXISTÊNCIA DE CPF
def ler_cpf(cpf):
    comando = f'SELECT cpf FROM tb_usuarios WHERE cpf = "{cpf}"'
    cursor.execute(comando)
    resultado = cursor.fetchall()
    return resultado

#LOGIN
def consultar_login(email, senha):
    cod_sql = 'SELECT senha from tb_usuarios WHERE email LIKE "%'+email+'%"'
    cursor.execute(cod_sql)
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        return None
    elif senha in resultado[0]:
        return True 
    else: 
        return False

# TERMINAR CRUD

if __name__ == '__main__':
    cpf = input('Digite o CPF: ')
    print(ler_cpf(cpf))
