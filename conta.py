#cada conta vai ter a tupla (numero, cpf_cliente, codigo_agencia, login, senha, saldo)
#o contado aqui embaixo comeca em 1 e serve pra cada conta ganhar um numero diferente quando for criada, nada dms
contas=[]
proximo_numero_conta = 1

#como o cpf ja identifica o cliente, eu optei por tirar o nome do cliente dessa funcao ok
#nao tenho muito q falar sobre essa funcao, é a mesma de antes mas alterada, tem o global ali pra poder modificar quem ta fora da funcao, monta a tupla e tem o saldo inicial de 1000.0
def criacao_de_conta(cpf, codigo_agencia, login, senha):
    global proximo_numero_conta
    
    nova_conta = (proximo_numero_conta, cpf, codigo_agencia, login, senha, 1000.0)
    contas.append(nova_conta)
    proximo_numero_conta = proximo_numero_conta + 1
    return nova_conta

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
        maior_numero = contas[0][0]
        for conta in contas:
            if conta[0] > maior_numero:
                maior_numero = conta[0]
        proximo_numero_conta = maior_numero + 1
        
#percorre a lista procurando uma conta pelo numero dela
def buscar_conta_por_numero(numero):
    for conta in contas:
        if conta[0] == numero:
            return conta
    return None

#essa funcao aqui me deu orgulho, ela basicamente serve pra gente atualizar o saldo, so que uma tupla é imutavel, entao basicamente ela percorre a lista procurando a conta que precisa ser alterada, monta uma tupla nova com as mesmas informacoes e mas altera o saldo e substitui a conta q tava antes 
def indice_da_conta(numero):
    for indice in range (len(contas)):
        if contas[indice][0] == numero:
            return indice
    return -1

#imprime uma lista, legal ne
def listar_contas():
    if len(contas) == 0:
        print("Nenhuma conta cadastrada")
        return
    print("\n------- CONTAS -------")
    for conta in contas:
        numero = conta[0]
        cpf = conta[1]
        codigo_agencia= conta[2]
        saldo = conta[5]
        print("Conta:", numero, " CPF:", cpf, " Agência:", codigo_agencia, "Saldo: R$", saldo)

#busca a conta e devolve o saldo
def consultar_saldo(numero_conta):
    conta = buscar_conta_por_numero(numero_conta)
    if conta is None:
        print("Conta nao encontrada")
        return None
    return conta[5]

#procura o indice da conta. Se o valor for positivo ele faz tudo aquuilo de montar uma tupla nova e substituir na lista, e retorna true e false 
def depositar(numero_conta, valor):
    indice = indice_da_conta(numero_conta)
    if indice == -1:
        print("conta nao encontrada")
        return False
    if valor > 0:
        conta_atual = contas[indice]
        conta_atualizada = (conta_atual[0] , conta_atual[1], conta_atual[2], conta_atual[3],  conta_atual[4], conta_atual[5] + valor)
        contas[indice] = conta_atualizada
        return True
    else:
        print("valor de deposito invalido")
        return False
#mesma coisa do debosito so q ao contrario
def sacar(numero_conta, valor):
    indice = indice_da_conta(numero_conta)
    if indice == -1:
        print("Conta não encontrada!")
        return False
 
    conta_atual = contas[indice]
    saldo_atual = conta_atual[5]
 
    if valor > 0 and valor <= saldo_atual:
        conta_atualizada = (conta_atual[0], conta_atual[1], conta_atual[2], conta_atual[3], conta_atual[4], saldo_atual - valor)
        contas[indice] = conta_atualizada
        return True
    else:
        print("Saldo insuficiente ou valor inválido!")
        return False

#acha os indices de origem e destino, confere se a conta de origem tem saldo sulficiente, se tudo tiver certo ela vai criar duas tuplas diferentes pra substituir os saldos, e basicamente um saque de um lado e um deposito do outro
def transferir(numero_conta_origem, numero_conta_destino, valor):
    indice_origem = indice_da_conta(numero_conta_origem)
    indice_destino = indice_da_conta(numero_conta_destino)
    if indice_origem == -1 or indice_destino == -1:
        print("conta de origem ou destino nao encontrada")
        return False
    conta_origem = contas[indice_origem]
    conta_destino= contas[indice_destino]
    saldo_origem = conta_origem[5]
    if valor > 0 and valor <= saldo_origem:
        conta_origem_atualizada = (conta_origem[0], conta_origem[1], conta_origem[2], conta_origem[3], conta_origem[4], saldo_origem - valor)
        conta_destino_atualizada = (conta_destino[0], conta_destino[1], conta_destino[2], conta_destino[3], conta_destino[4], conta_destino[5] + valor)
        contas[indice_origem] = conta_origem_atualizada
        contas[indice_destino] = conta_destino_atualizada
        return True
    else:
        print("Saldo insuficiente ou valor inválido!")
        return False

#percorre todas as contas e soma o saldo
def montante_total_banco():
    total = 0
    for conta in contas:
        total = total + conta[5]
    return total
