#cada conta vai ter a tupla (numero, cpf_cliente, codigo_agencia, login, senha, saldo)
#o contado aqui embaixo comeca em 1 e serve pra cada conta ganhar um numero diferente quando for criada, nada dms
contas=[]
proximo_numero_conta = 1

#como o cpf ja identifica o cliente, eu optei por tirar o nome do cliente dessa funcao ok
#nao tenho muito q falar sobre essa funcao, é a mesma de antes mas alterada, tem o global ali pra poder modificar quem ta fora da funcao, monta a tupla e tem o saldo inicial de 1000.0
def criacao_de_conta(cpfs, codigo_agencia, login, senha, tipo):
    global proximo_numero_conta

    contas_criadas = []

    for cpf in cpfs:

        if tipo not in ["salário", "corrente", "poupança"]:
            print("Tipo de conta inválido!")
            return None

        nova_conta = {"numero": proximo_numero_conta, "cpf": cpf, "codigo_agencia": codigo_agencia, "login": login, "senha": senha, "saldo": 0.0, "tipo": tipo}

        contas.append(nova_conta)
        contas_criadas.append(nova_conta)

        proximo_numero_conta = proximo_numero_conta + 1

    return contas_criadas

#substitui a lista inteira de contas por outra
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

#essa funcao aqui me deu orgulho, ela basicamente serve pra gente atualizar o saldo, so que uma tupla é imutavel, entao basicamente ela percorre a lista procurando a conta que precisa ser alterada, monta uma tupla nova com as mesmas informacoes e mas altera o saldo e substitui a conta q tava antes 
def indice_da_conta(numero):
    for indice in range(len(contas)):
        if contas[indice]["numero"] == numero:
            return indice
    return -1

#imprime uma lista, legal ne
def listar_contas():
    if len(contas) == 0:
        print("Nenhuma conta cadastrada")
        return
    print("\n------- CONTAS -------")
    for conta in contas:
        print("Conta:", conta["numero"],
              " CPF:", conta["cpf"],
              " Agência:", conta["codigo_agencia"],
              " Tipo:", conta["tipo"],
              " Saldo: R$", conta["saldo"])

#busca a conta e devolve o saldo
def consultar_saldo(numero_conta):
    conta = buscar_conta_por_numero(numero_conta)
    if conta is None:
        print("Conta nao encontrada")
        return None
    return conta["saldo"]

#procura o indice da conta. Se o valor for positivo ele faz tudo aquuilo de montar uma tupla nova e substituir na lista, e retorna true e false 
def depositar(numero_conta, valor):
    conta = buscar_conta_por_numero(numero_conta)
    if conta is None:
        print("conta não encontrada")
        return False
    if valor > 0:
        conta["saldo"] += valor
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
        return True
    print("Saldo insuficiente ou valor inválido!")
    return False

#acha os indices de origem e destino, confere se a conta de origem tem saldo sulficiente, se tudo tiver certo ela vai criar duas tuplas diferentes pra substituir os saldos, e basicamente um saque de um lado e um deposito do outro
def transferir(numero_conta_origem, numero_conta_destino, valor):
    origem = buscar_conta_por_numero(numero_conta_origem)
    destino = buscar_conta_por_numero(numero_conta_destino)
    if origem is None or destino is None:
        print("Conta de origem ou destino não encontrada!")
        return False
    if valor > 0 and valor <= origem["saldo"]:
        origem["saldo"] -= valor
        destino["saldo"] += valor
        return True
    print("Saldo insuficiente ou valor inválido!")
    return False

#percorre todas as contas e soma o saldo
def montante_total_banco(contas):
    total = 0.0
    for conta in contas:
        total += conta["saldo"]
    return total
