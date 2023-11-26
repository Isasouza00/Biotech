import hashlib
import socket
import database


def obter_dominio():
    nome_host = socket.gethostname()
    dominio = socket.getfqdn(nome_host)
    return dominio

def consulta_cpf(cpf):
    cpf = str(cpf)
    digito_verificador1 = 0
    digito_verificador2 = 0
    checagem_dv1 = 0
    checagem_dv2 = 0

    # verificar número de caracteres
    if len(cpf) < 11:
        diferença_cpf = 11 - len(cpf)
        cpf = ('0' * diferença_cpf) + cpf
    
    # capturar número verificador
    checagem_dv1 = int(cpf[9:10])
    checagem_dv2 = int(cpf[10:11])
    
    #calculo do primeiro digito verificador
    for c in range(1, 10):
        digito_verificador1 += int(cpf[c-1:c]) * c
    
    #pegando resto da divisão  do digito verificador 1 por 11
    digito_verificador1 %= 11

    #se número for maior que 10 considerar 0
    if (digito_verificador1 == 10):
        digito_verificador1 = 0

    #calculo do primeiro digito verificador
    for c in range(2, 11):
        digito_verificador2 += int(cpf[c-1:c]) * (c-1)
    
    #pegando resto da divisão  do digito verificador 1 por 11
    digito_verificador2 %= 11

    #se número for maior que 10 considerar 0
    if (digito_verificador2 == 10):
        digito_verificador2 = 0

    if (digito_verificador1 == checagem_dv1 and digito_verificador2 == checagem_dv2):
        return True
    else:
        return False

def criptografa_senha(senha):
    hashed = hashlib.md5(senha.encode('utf-8'))
    return hashed.hexdigest()

def url_usuario(email):
    hashed = hashlib.md5(email.encode('utf-8'))
    return hashed.hexdigest()

# def verificar_horario(datas_formatadas, horarios_formatados):
#     if datas_formatadas in data_escolhida and horarios_formatados in horario_escolhido:
#         return 0
#     else: return 1
# if __name__ == '__main__':
#     print(verificar_horario(database.consultar_horarios('Dr. Ricardo Santos')[0], database.consultar_horarios('Dr. Ricardo Santos')[1]))
































