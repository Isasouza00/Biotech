from flask import Flask, render_template, redirect, request
import database
import consulta_cpf

try:
    database.conexao
except database.mysql.connector.Error:
    print('erro')

app = Flask(__name__)

# PÁGINA CADASTRO
@app.route('/')
def input():
    return render_template('home.html')

# PÁGINA DE CADASTRO
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastrar():
    render_template('cadastro.html')
    #CAPTURANDO INPUTS DO FORMULÁRIO
    if request.method == 'POST':
        nome = request.form.get('cadastro_nome').lower()
        cpf = request.form.get('cadastro_cpf')
        email = request.form.get('cadastro_email').lower()
        senha = request.form.get('cadastro_senha')
        confirmaçao_senha = request.form.get('confirmaçao_senha')

        #VERIFICAR CONDIÇÕES PARA ACEITE DO CADASTRO (CAMPOS COMPLETOS, SENHAS BATENDO, CPF VÁLIDO...)
        while True:
            if (nome == '' or cpf == '' or email == '' or senha == '' or confirmaçao_senha == ''):
                erro = 'PREENCHA TODOS OS CAMPOS'
                return render_template('cadastro.html', erro = erro)
            else:
                break

        if consulta_cpf.consulta_cpf(cpf) == True:
            if len(senha) < 8 or senha.isalnum == False:
                erro = 'A SENHA DEVE CONTER 8 CARACTERES E SER ALFANUMÉRICA'
                return render_template('cadastro.html', erro = erro)
            if confirmaçao_senha == senha:
                database.inserir_usuario(nome, cpf, email, senha)
                return render_template('login.html')
            else:
                erro = 'AS SENHAS SÃO DIFERENTES'
                return render_template('cadastro.html', erro = erro)
        else:
            erro = 'CPF INVÁLIDO'
            return render_template('cadastro.html', erro = erro)

# RODANDO SITE
if __name__ == '__main__':
    app.run(debug=True)