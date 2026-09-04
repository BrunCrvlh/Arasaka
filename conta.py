def criacao_de_conta(cliente, cpf):
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
