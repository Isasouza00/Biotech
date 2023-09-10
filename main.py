from flask import Flask, render_template, redirect, request, flash
import database
import consulta_cpf

try:
    database.conexao
except database.mysql.connector.Error:
    print('erro')

app = Flask(__name__)
app.config['SECRET_KEY'] = "BIOTECH"

# PÁGINA CADASTRO
@app.route('/')
def input():
    return render_template('home.html')

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

#VERIFICAR CONDIÇÕES PARA ACEITE DO CADASTRO
def confirmaçoes(nome, cpf, email, senha, confirmaçao_senha):
    # IMPLEMENTAR CONFIRMAÇÃO DE CPF DUPLICADO

    #VERIFICA SE CAMPOS ESTÃO PREENCHIDOS
    while True:
        if (nome == '' or cpf == '' or email == '' or senha == '' or confirmaçao_senha == ''):
            erro = 'PREENCHA TODOS OS CAMPOS'
            flash(erro)
            return redirect('/cadastro')
        else:
            break
    # VERIFICA SE CPF É VALOR VÁLIDO (SE POSSÍVEL IMPLEMENTAR API)
    if consulta_cpf.consulta_cpf(cpf) == True:
        if len(senha) < 8 or senha.isalnum == False:
            erro = 'A SENHA DEVE CONTER 8 CARACTERES E SER ALFANUMÉRICA'
            flash(erro)
            return redirect('/cadastro')
        # VERIFICA SE SENHA E CONFIRMAÇÃO DE SENHA ESTÃO BATENDO
        if confirmaçao_senha == senha:
            database.inserir_usuario(nome, cpf, email, senha)
            return redirect('/login')
        else:
            erro = 'AS SENHAS SÃO DIFERENTES'
            flash(erro)
            return redirect('/cadastro')
    else:
        erro = 'CPF INVÁLIDO'
        flash(erro)
        return redirect('/cadastro')

# PÁGINA DE LOGIN
@app.route('/login')
def login():
    return render_template('login.html')

# RODANDO SITE
if __name__ == '__main__':
    app.run(debug=True)