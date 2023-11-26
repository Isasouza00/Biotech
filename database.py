# IMPORTANDO BIBLIOTECAS
import mysql.connector
import datetime

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

def ler_senha():
    comando = f'SELECT senha FROM tb_usuarios WHERE id_usuario = "1"'
    cursor.execute(comando)
    resultado = cursor.fetchall()
    return print(resultado)

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

# VERIFICA SE É ADMIN
def verificar_admin (email):
    if "@biotech" in email:
        return True
    else: 
        return False
    
# CONSULTAR CONSULTAS
def consultar_consultas(paciente):
    cod_sql = 'SELECT * from tb_consultas WHERE paciente LIKE "%'+paciente+'%"'
    cursor.execute(cod_sql)
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        return None
    else: 
        return resultado

# AGENDAR CONSULTAS
def agendar(paciente, data, profissional, especialidade, observação):
    cod_sql = '''INSERT INTO tb_consultas (paciente, data, profissional, especialidade, observação) VALUES ("{paciente}",
    "{data}", "{profissional}", "{especialidade}", "{observação}")'''
    cursor.execute(cod_sql)

# Consultar horários
def consultar_horarios(profissional):
    cod_sql = 'SELECT data, horario from tb_consultas WHERE profissional LIKE "%'+profissional+'%"'
    cursor.execute(cod_sql)
    resultado = cursor.fetchall()
    lista_datas = []
    lista_horarios = []
    for c in range (0, len(resultado)):
        acesso = resultado[c]
        data = acesso[0]
        horario = acesso[1]
        lista_datas.append(data)
        lista_horarios.append(horario)
    datas_formatadas = [data.strftime('%Y-%m-%d') for data in lista_datas]
    lista_segundos = [str(int(t.total_seconds())) for t in lista_horarios]
    horarios_formatados = [str(datetime.timedelta(seconds=int(s))) for s in lista_segundos]
    horarios_formatados = [':'.join(h.split(':')[:2]) for h in horarios_formatados]
    return datas_formatadas, horarios_formatados

#Consultar nome
def consultar_nome(paciente):
    cod_sql = 'SELECT nome from tb_usuarios WHERE paciente LIKE "%'+paciente+'%"'
    cursor.execute(cod_sql)
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        return False
    else: 
        return True

# TERMINAR CRUD
if __name__ == '__main__':
    print(consultar_horarios('Dr. Ricardo Santos'))