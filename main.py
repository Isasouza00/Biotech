from flask import Flask, render_template, redirect, request, flash, url_for
from datetime import date
import database
import funções

#FUNÇÃO PARA VERIFICAR CONDIÇÕES PARA ACEITE DO CADASTRO
def confirmaçoes(nome, cpf, email, senha, confirmaçao_senha):
    # IMPLEMENTAR CONFIRMAÇÃO DE CPF DUPLICADO
    #EXEMPLO PRA LIVIA VER
    #VERIFICA SE CAMPOS ESTÃO PREENCHIDOS
    while True:
        if (nome == '' or cpf == '' or email == '' or senha == '' or confirmaçao_senha == ''):
            erro = 'PREENCHA TODOS OS CAMPOS'
            flash(erro)
            return redirect('/cadastro')
        else:
            break
    # VERIFICA SE CPF É VALOR VÁLIDO
    if funções.consulta_cpf(cpf) == True:
        if len(database.ler_cpf(cpf)) > 0:
            erro = 'CPF JÁ CADASTRADO'
            flash(erro)
            return redirect('/cadastro')
        if len(senha) < 8 or senha.isalnum == False:
            erro = 'A SENHA DEVE CONTER 8 CARACTERES E SER ALFANUMÉRICA'
            flash(erro)
            return redirect('/cadastro')
        # VERIFICA SE SENHA E CONFIRMAÇÃO DE SENHA ESTÃO BATENDO
        if confirmaçao_senha == senha:
            database.inserir_usuario(nome, cpf, email, funções.criptografa_senha(senha))
            return redirect('/login')
        else:
            erro = 'AS SENHAS SÃO DIFERENTES'
            flash(erro)
            return redirect('/cadastro')
    else:
        erro = 'CPF INVÁLIDO'
        flash(erro)
        return redirect('/cadastro')

# CONECTANDO AO DB
try:
    database.conexao
except database.mysql.connector.Error:
    print('erro')

#DECLARANDO APP
app = Flask(__name__)
app.config['SECRET_KEY'] = "BIOTECH"

# PÁGINA HOME
@app.route('/')
def home():
    return render_template('cadastro.html')

# PÁGINA DE CADASTRO
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

#PÁGINA QUE RECEBE DADOS DO CADASTRO
@app.route('/cadastro', methods=['POST'])
def cadastrar():
    #CAPTURANDO INPUTS DO FORMULÁRIO
    if request.method == 'POST':
        nome = request.form.get('cadastro_nome').lower()
        cpf = request.form.get('cadastro_cpf')
        email = request.form.get('cadastro_email').lower()
        senha = request.form.get('cadastro_senha')
        confirmaçao_senha = request.form.get('confirmaçao_senha')
        return confirmaçoes(nome, cpf, email, senha, confirmaçao_senha)

# PÁGINA DE LOGIN
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def logar():
    if request.method == 'POST':
        email = request.form.get('login_email')
        senha = funções.criptografa_senha(request.form.get('login_senha'))
        nome = database.consultar_nome_por_email(email)
        while True:
            if (email == '' or senha == ''):
                erro = 'PREENCHA TODOS OS CAMPOS'
                flash(erro)
                return redirect('/login')
            else:
                break
        if database.consultar_login(email, senha) == True:
            if database.verificar_admin(email) == True:
                if ".senacsp.edu.br" in funções.obter_dominio():
                    return redirect(url_for('consultas_adm', usuario = funções.url_usuario(email)+000000000000))
                    erro = 'Você precisa estar conectado na empresa para acessar login de administrador'
                    flash(erro)
                    return redirect('/login')
            else:
                return redirect(url_for('consultas', usuario = funções.url_usuario(email)))
        elif database.consultar_login(email, senha) == False:
            erro = 'Email ou senha incorretos'
            flash(erro)
            return redirect('/login')
        elif database.consultar_login(email, senha) == None:
            erro = 'Email não encontrado'
            flash(erro)
            return redirect('/login')

# g_nome = logar()[1]

# PÁGINA DE CONSULTAS DO USUÁRIO
@app.route('/<usuario>/consultas')
def consultas(usuario):
    lista_exames = database.lista_exames()
    return render_template('consultas.html', lista_exames=lista_exames)

# @app.route('/<usuario>/consultas', methods=['POST'])
# def marcar():
#     # capturar dados do formulário
#     horario = funções.verificar_horario(database.consultar_horarios(profissional)[0], database.consultar_horarios(profissional)[1])
#     if horario == 0:
#         vai sumir
#     else: roda função de marcar

# PÁGINA DE EXAMES DO USUÁRIO
@app.route('/<usuario>/exames')
def exames(usuario):
    # database.recolher_exames(g_nome)
    return render_template('exames.html')


@app.route('/<usuario>/consultas_adm')
def consultas_adm(usuario):
    return render_template('consultas_adm.html')

# IMPLEMENTAR DIGITOO VERIFICADOR!
@app.route('/<usuario>/exames_adm')
def exames_adm(usuario):
    if usuario == 000000000000:
        return render_template('exames_adm.html')
    else: return render_template('login.html')

# @app.route('/<usuario>/exames_adm', methods=['POST'])
# def lançar_exame():
#     if request.method == 'POST':
#             # capturar dados do formulário
#         while True:
#             if paciente == '' or tipo_exame == '' or exame == '':
#                 erro = 'PREENCHA TODOS OS CAMPOS'
#                 flash(erro)
#                 return redirect(url_for('lançar_exame')) #talvez aqui tenha que vir o link dinâmico do usuário
#             else:
#                 break
#         if database.consultar_nome == False:
#             erro = 'ESSE PACIENTE NÃO EXISTE'
#             flash(erro)
#             return redirect(url_for('lançar_exame')) #talvez aqui tenha que vir o link dinâmico do usuário
#         else:
#             database.inserir_exames(paciente, date.today(), profissional, tipo_exame, exame)

# RODANDO SITE
if __name__ == '__main__':
    app.run(debug=True)

