# Lista de agências
# Cada agência é uma tripla: (codigo, nome, cidade)
agencias = []


# Cadastra um nova agência e verifica se o código já existe
def criar_agencia(codigo, nome, cidade):
    if buscar_agencia_por_codigo(codigo) is not None:
        print("Código de agência já cadastrado!")
        return None

    nova_agencia = (codigo, nome, cidade)
    agencias.append(nova_agencia)

    return nova_agencia
    
#substitui a lista inteira de agências por outra
def definir_agencias(lista):
    global agencias
    agencias.clear()
    agencias.extend(lista)

# Procura uma agência pelo código
def buscar_agencia_por_codigo(codigo):
    for agencia in agencias:
        if agencia[0] == codigo:
            return agencia

    return None


# Mostra todas as agências cadastradas
def listar_agencias():
    if len(agencias) == 0:
        print("Nenhuma agência cadastrada.")
        return

    print("\n------- AGÊNCIAS -------")

    for agencia in agencias:
        print("Código:", agencia[0], "| Nome:", agencia[1],"| Cidade:", agencia[2])
        
# Calcula o dinheiro total das contas pertencentes à agência
def montante_total_agencia(codigo, contas):
    total = 0.0

    for conta in contas:
        # conta[2] é o código da agência e conta[5] é o saldo.
        if conta[2] == codigo:
            total = total + conta[5]

    return total
