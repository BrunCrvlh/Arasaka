#cada conta vai ter a tupla (numero, cpf_cliente, codigo_agencia, login, senha, saldo)
#o contado aqui embaixo comeca em 1 e serve pra cada conta ganhar um numero diferente quando for criada, nada dms
from datetime import datetime

contas=[]
proximo_numero_conta = 1

#guarda uma linha no extrato da conta (valor positivo entra dinheiro, negativo sai)
def registrar(conta, tipo, valor, descricao):
    if "extrato" not in conta:
        conta["extrato"] = []
    conta["extrato"].append({"data": datetime.now().strftime("%d/%m/%Y %H:%M"), "tipo": tipo, "valor": valor, "descricao": descricao})


#nao tenho muito q falar sobre essa funcao, tem o global ali pra poder modificar quem ta fora da funcao e plau, faz as verificacoes dela e cria a conta
def criacao_de_conta(cpfs, codigo_agencia, login, senha, tipo):
    global proximo_numero_conta

    contas_criadas = []

    for cpf in cpfs:

        if tipo not in ["salário", "corrente", "poupança"]:
            print("Tipo de conta inválido!")
            return None

        nova_conta = {"numero": proximo_numero_conta, "cpf": cpf, "codigo_agencia": codigo_agencia, "login": login, "senha": senha, "saldo": 0.0, "tipo": tipo, "extrato": []}

        contas.append(nova_conta)
        contas_criadas.append(nova_conta)

        proximo_numero_conta = proximo_numero_conta + 1

    return contas_criadas

#ajeita o proximo_numero_conta, pra nao repetir o numero de conta depois de carregar os dados  
def definir_contas(lista):
    global contas
    global proximo_numero_conta

    contas.clear()
    contas.extend(lista)

    if len(contas) == 0:
        proximo_numero_conta = 1
    else:
        maior_numero = contas[0]["numero"]
        for conta in contas:
            if conta["numero"] > maior_numero:
                maior_numero = conta["numero"]
        proximo_numero_conta = maior_numero + 1
        
#percorre a lista procurando uma conta pelo numero dela
def buscar_conta_por_numero(numero):
    for conta in contas:
        if conta["numero"] == numero:
            return conta
    return None

#procura o indice da conta. Se o valor for positivo ele faz tudo aquuilo de montar uma tupla nova e substituir na lista, e retorna true e false 
def depositar(numero_conta, valor):
    conta = buscar_conta_por_numero(numero_conta)
    if conta is None:
        print("conta não encontrada")
        return False
    if valor > 0:
        conta["saldo"] += valor
        registrar(conta, "DEPÓSITO", valor, "Depósito em conta")
        return True
    print("valor de depósito inválido")
    return False
    
#mesma coisa do debosito so q ao contrario
def sacar(numero_conta, valor):
    conta = buscar_conta_por_numero(numero_conta)
    if conta is None:
        print("Conta não encontrada!")
        return False
    if valor > 0 and valor <= conta["saldo"]:
        conta["saldo"] -= valor
        registrar(conta, "SAQUE", -valor, "Saque")
        return True
    print("Saldo insuficiente ou valor inválido!")
    return False

#acha os indices de origem e destino, ai saca de um lado e deposita do outro, nada demais,
def transferir(numero_conta_origem, numero_conta_destino, valor):
    origem = buscar_conta_por_numero(numero_conta_origem)
    destino = buscar_conta_por_numero(numero_conta_destino)
    if origem is None or destino is None:
        print("Conta de origem ou destino não encontrada!")
        return False
    if valor > 0 and valor <= origem["saldo"]:
        origem["saldo"] -= valor
        destino["saldo"] += valor
        registrar(origem, "TRANSFERÊNCIA", -valor, "Enviado para a conta " + str(destino["numero"]))
        registrar(destino, "TRANSFERÊNCIA", valor, "Recebido da conta " + str(origem["numero"]))
        return True
    print("Saldo insuficiente ou valor inválido!")
    return False

#percorre todas as contas e soma o saldo
def montante_total_banco():
    total = 0.0
    for conta in contas:
        total += conta["saldo"]
    return total
