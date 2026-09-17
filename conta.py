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

