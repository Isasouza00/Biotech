from flask import Flask, render_template, redirect, request, flash, url_for
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
                    return redirect(url_for('consultas_adm', usuario = 000000000000))
                else:
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
        
# PÁGINA DE CONSULTAS DO USUÁRIO
@app.route('/<usuario>/consultas')
def consultas(usuario):
    return render_template('consultas.html')

# PÁGINA DE EXAMES DO USUÁRIO
@app.route('/<usuario>/exames')
def exames(usuario):
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
# RODANDO SITE
if __name__ == '__main__':
    app.run(debug=True)

