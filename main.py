from flask import Flask, render_template, redirect, request, flash, url_for
import database
import funções
import datetime

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

# PÁGINA HOME/CADASTRO
@app.route('/')
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
    global g_nome
    if request.method == 'POST':
        email = request.form.get('login_email')
        senha = funções.criptografa_senha(request.form.get('login_senha'))
        g_nome = database.consultar_nome_por_email(email)[0][0]
        while True:
            if (email == '' or senha == ''):
                erro = 'PREENCHA TODOS OS CAMPOS'
                flash(erro)
                return redirect('/login')
            else:
                break
        if database.consultar_login(email, senha) == True:
            if database.verificar_admin(email) == True:
                if "Mathbook" == funções.obter_dominio():
                    return redirect(url_for('novo_exame', usuario = funções.url_usuario(email)+'4062696f746563682e636f6d', g_nome = g_nome))
                else:
                    erro = 'Você precisa estar conectado na empresa para acessar login de administrador'
                    flash(erro)
                    return redirect('/login')
            else:
                return redirect(url_for('tabela_exames', usuario = funções.url_usuario(email), g_nome = g_nome))
        elif database.consultar_login(email, senha) == False:
            erro = 'Email ou senha incorretos'
            flash(erro)
            return redirect('/login')
        elif database.consultar_login(email, senha) == None:
            erro = 'Email não encontrado'
            flash(erro)
            return redirect('/login')
        
@app.route('/<usuario>/calendario_consultas_adm')
def calendario_consultas_adm(usuario):
    if '4062696f746563682e636f6d' in usuario:
        return render_template('calendario_consultas_adm.html', usuario = usuario)
    else:
        return redirect('/login')

@app.route('/<usuario>/calendario_consultas_adm', methods=['POST'])
def consultas_adm(usuario):
    for c in range(1, 32):
        botão = request.form.get(c)
        botão = int(botão)
        return render_template('calendario_consultas_adm.html', usuario = usuario, botão = botão, lista_datas = database.data_consulta(g_nome))

############################################################################################################################################################################################
@app.route('/<usuario>/nova_consulta')
def formulario_consultas(usuario):
    if '4062696f746563682e636f6d' in usuario:
        return render_template('nova_consulta.html', usuario = usuario, g_nome = g_nome)
    else:
        return redirect('/login')

@app.route('/<usuario>/nova_consulta', methods=['POST'])
def lançar_consulta(usuario):
    if request.method == 'POST':
        data_hora = request.form.get('datemax').replace('T', ' ')
        paciente = request.form.get('name_usu')
        while True:
            if paciente == '' or data_hora == '':
                erro = 'PREENCHA TODOS OS CAMPOS'
                flash(erro)
                return redirect(url_for('formulario_consultas', usuario = usuario, g_nome = g_nome))#talvez aqui tenha que vir o link dinâmico do usuário
            else:
                break 
        if database.consultar_nome(paciente) == False:
            erro = 'O PACIENTE NÃO POSSUI CADASTRO'
            flash(erro)
            return redirect(url_for('formulario_consultas', usuario = usuario, g_nome = g_nome)) #talvez aqui tenha que vir o link dinâmico do usuário
        else:
            database.agendar(paciente, data_hora, g_nome, g_nome)
            erro = 'CONSULTA ADICIONADA COM SUCESSO!!'
            flash(erro)
            return redirect(url_for('formulario_consultas', usuario = usuario, g_nome = g_nome))

@app.route('/<usuario>/calendario_consultas')
def calendario_consultas(usuario):
        return render_template('calendario_consultas.html', usuario = usuario, g_nome = g_nome)

@app.route('/<usuario>/calendario_consultas', methods=['POST'])
def consultas(usuario):
    for c in range(1, 32):
        botão = request.form.get(c)
        botão = int(botão)
        return render_template('calendario_consultas.html', usuario = usuario, botão = botão, lista_datas = database.data_consulta(g_nome))
############################################################################################################################################################################################

# PÁGINA DE EXAMES DO USUÁRIO
@app.route('/<usuario>/tabela_exames')
def tabela_exames(usuario):
    return render_template('tabela_exames.html', usuario = usuario, tupla_exames = database.recolher_exames(g_nome))

@app.route('/<usuario>/tabela_exames_adm')
def tabela_exames_adm(usuario):
    if '4062696f746563682e636f6d' in usuario:
        return render_template('tabela_exames_adm.html', usuario = usuario, tupla_exames = database.recolher_exames_adm(g_nome))
    else:
        return redirect('/login')

@app.route('/<usuario>/novo_exame')
def novo_exame(usuario):
    if '4062696f746563682e636f6d' in usuario:
        return render_template('novo_exame.html', lista_exames = database.lista_exames(), usuario = usuario)
    else:
        return redirect('/login')
    
@app.route('/<usuario>/novo_exame', methods=['POST'])
def lançar_exame(usuario):
    if request.method == 'POST':
        exame = request.form.get('especialidade')
        data = request.form.get('datemax')
        paciente = request.form.get('name_usu')
        link = request.form.get('url')
        while True:
            if paciente == '' or exame == '' or link == '' or data == '':
                erro = 'PREENCHA TODOS OS CAMPOS'
                flash(erro)
                return redirect(url_for('novo_exame', usuario = usuario))#talvez aqui tenha que vir o link dinâmico do usuário
            else:
                break 
        if database.consultar_nome(paciente) == False:
            erro = 'O PACIENTE NÃO POSSUI CADASTRO'
            flash(erro)
            return redirect(url_for('novo_exame', usuario = usuario)) #talvez aqui tenha que vir o link dinâmico do usuário
        else:
            database.inserir_exames(paciente, data, g_nome, exame, link)
            erro = 'EXAME ENVIADO COM SUCESSO!!'
            flash(erro)
            return redirect(url_for('novo_exame', usuario = usuario, g_nome = g_nome))

# RODANDO SITE
if __name__ == '__main__':
    app.run(debug=True)

