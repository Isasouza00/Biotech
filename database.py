# IMPORTANDO BIBLIOTECAS
import mysql.connector
import datetime

# CONECTANDO AO DB BIOTECH
conexao = mysql.connector.connect(host='localhost', user='root',
                                  password='admin', database='biotechdb')

# CRIANDO CURSOR
cursor = conexao.cursor()

def data_consulta(profissional):
    cod_sql = 'SELECT data from tb_consulta WHERE profissional = "%'+profissional+'%"'
    cursor.execute(cod_sql)
    resultado = cursor.fetchall()
    lista_datas = [item[0][-2:] for item in resultado]
    return lista_datas

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
    cod_sql = 'SELECT * from tb_consulta WHERE paciente LIKE "%'+paciente+'%"'
    cursor.execute(cod_sql)
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        return None
    else: 
        return resultado
    
def buscar_especialidade(profissional):
    cod_sql = 'SELECT Especialidade from tb_medicos WHERE Nome LIKE "%'+profissional+'%"'
    cursor.execute(cod_sql)
    resultado = cursor.fetchall()
    especialidade = [item[0] for item in resultado]
    return especialidade

# AGENDAR CONSULTAS
def agendar(paciente, data_hora, profissional, especialidade):
    cod_sql = '''INSERT INTO tb_consulta (paciente, data_hora, profissional, especialidade) VALUES ("{paciente}",
    "{data_hora}", "{profissional}", "{especialidade}")'''
    return cursor.execute(cod_sql)

# Consultar horários
def consultar_horarios(profissional):
    cod_sql = 'SELECT data, horario from tb_consulta WHERE profissional LIKE "%'+profissional+'%"'
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
    cod_sql = 'SELECT nome from tb_usuarios WHERE nome LIKE "%'+paciente+'%"'
    cursor.execute(cod_sql)
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        return False
    else: 
        return True
    
#Consultar nome
def consultar_nome_por_email(email):
    cod_sql = 'SELECT nome from tb_usuarios WHERE email LIKE "%'+email+'%"'
    cursor.execute(cod_sql)
    resultado = cursor.fetchall()
    return resultado

def inserir_exames(paciente, data, profissional, exame, link):
    comando = f'INSERT INTO tb_exames (paciente, data, profissional, tipo_exame, exame) VALUES ("{paciente}", "{data}", "{profissional}", "{exame}", "{link}")'
    cursor.execute(comando)
    conexao.commit()

def lista_exames():
    cod_sql = 'SELECT Nome from tb_exames_disponiveis'
    cursor.execute(cod_sql)
    resultado = cursor.fetchall()
    lista_exames = [item[0] for item in resultado]
    return lista_exames

def recolher_exames_adm(nome):
    cod_sql = 'SELECT id_exames, paciente, data, tipo_exame, exame from tb_exames WHERE profissional LIKE "%'+nome+'%"'
    cursor.execute(cod_sql)
    tupla_exames = cursor.fetchall()
    return tupla_exames

def recolher_exames(nome):
    cod_sql = 'SELECT id_exames, data, profissional, tipo_exame, exame from tb_exames WHERE paciente LIKE "%'+nome+'%"'
    cursor.execute(cod_sql)
    tupla_exames = cursor.fetchall()
    return tupla_exames

def lista_especialidades():
    cod_sql = 'SELECT especialidade from tb_medicos'
    cursor.execute(cod_sql)
    resultado = cursor.fetchall()
    lista_especialidades = [item[0] for item in resultado]
    return lista_especialidades

# TERMINAR CRUD
if __name__ == '__main__':
    print(verificar_admin('livia.clima@biotech.com'))