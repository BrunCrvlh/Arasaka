#cada conta vai ter a tupla (numero, cpf_cliente, codigo_agencia, login, senha, saldo)

contas=[]
proximo_numero_conta = 1

#como o cpf ja identifica o cliente, eu optei por tirar o nome do cliente dessa funcao ok?
def criacao_de_conta(cpf:
    numero_da_conta = "2602079 - 55"
    nome = cliente
    login = "Bruno44"
    senha = "12345"
    saldo_atual = float(0)
    
    return numero_da_conta, cpf, nome, login, senha, saldo_atual

def consultar_saldo(saldo_atual):
    return saldo_atual
    
def depositar(saldo_atual, valor_de_deposito):
    if valor_de_deposito > 0:
        return saldo_atual + valor_de_deposito
    else:
        return saldo_atual
        
def sacar(saldo_atual, valor_de_saque):
    if valor_de_saque <= saldo_atual and valor_de_saque > 0:
        return saldo_atual - valor_de_saque
    else:
        return saldo_atual
