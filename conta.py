#cada conta vai ter a tupla (numero, cpf_cliente, codigo_agencia, login, senha, saldo)

contas=[]
proximo_numero_conta = 1

#como o cpf ja identifica o cliente, eu optei por tirar o nome do cliente dessa funcao ok
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

def indice_da_conta(numero):
    for indice in range (len(contas)):
        if contas[indice][0] == numero:
            return indice
    return -1

def listar_contas():
    if len(contas) == 0:
        print("Nenhuma conta cadastrada")
        return
        print("\n------- CONTAS -------")
        for conta in contas:
            numero = conta[0]
            cpf = conta[1]
            condigo_agencia= conta[2]
            saldo = conta[5]
            print("Conta:", numero, " CPF:", cpf, " Agência:", codigo_agencia, "Saldo: R$", Saldo)

def consultar_saldo(numero_cliente):
     conta = buscar_conta_por_numero(numero_conta)
    if conta is None::
        print("Conta nao encontrada")
        return None
    return conta[5]

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

def transferir(numero_conta_origem, numero_conta_destino, valor):
    indice_origem = _indice_da_conta(numero_conta_origem)
    indice_destino = _indice_da_conta(numero_conta_destino)
    if indice_origem == -1 or indice_destino == -1:
        print("conta de origem ou destino nao encontrada")
        return False
    conta_origem = contas[indice_origem]
    conta_destino= contas[indice_destino]
    saldo_origem = conta_origem[5]
    if valor > 0 and valor <= saldo_origem:
        conta_origem_atualizada = (conta_origem[0], conta_origem[1], conta_origem[2], conta_origem[3], conta_origem[4], saldo_origem - valor)
        conta_destino_atualizada = (conta_destino[0], conta_destino[1], conta_destino[2],conta_destino[3], conta_destino[4], conta_destino[5] + valor)contas[indice_origem] = conta_origem_atualizada
        contas[indice_destino] = conta_destino_atualizada
        return True
    else:
        print("Saldo insuficiente ou valor inválido!")
        return False

def montante_total_banco():
    total = 0
    for conta in contas:
        total = total + contas[5]
    return total
