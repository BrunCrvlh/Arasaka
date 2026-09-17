#cada conta vai ter a tupla (numero, cpf_cliente, codigo_agencia, login, senha, saldo)

contas=[]
proximo_numero_conta = 1

#como o cpf ja identifica o cliente, eu optei por tirar o nome do cliente dessa funcao ok?
def criacao_de_conta(cpf, codigo_agencia, login, senha):
    global proximo_numero_conta
    
    nova_conta = (proximo_numero_conta, cpf_cliente, codigo_agencia, login, senha, 0.0)
    contas.append(nova_conta)
    proximo_numero_conta = proximo_numero_conta + 1
    return nova_conta

def buscar_contar_por_numero(numero):
    for conta in contas:
        if conta[0] == numero:
            return conta
            return None

