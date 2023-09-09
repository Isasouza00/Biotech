from flask import Flask, render_template, redirect, request
import Conexão

try:
    Conexão.conexao
except Conexão.mysql.connector.Error:
    print('erro')

app = Flask(__name__)

# PÁGINA CADASTRO
@app.route('/')
def input():
    return render_template('cadastro.html')

# PÁGINA SUCCESS (TEMPORÁRIA)
@app.route('/cadastro', methods=['POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('cadastro_nome')
        cpf = request.form.get('cadastro_cpf')
        email = request.form.get('cadastro_email')
        senha = request.form.get('cadastro_senha')
        Conexão.inserir_usuario(nome, cpf, email, senha)
        return render_template('success.html')

# RODANDO SITE
if __name__ == '__main__':
    app.run(debug=True)

# TESTE COMMIT