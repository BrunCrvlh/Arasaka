# Lista de agências
# Cada agência é uma tripla: (codigo, nome, cidade)
agencias = []


# Cadastra um nova agência e verifica se o código já existe
def criar_agencia(codigo, nome, cidade):
    if buscar_agencia_por_codigo(codigo) is not None:
        print("Código de agência já cadastrado!")
        return None

    nova_agencia = {'Codigo da agencia': codigo,'Nome da agencia': nome, 'Cidade': cidade}
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
        if agencia['Codigo da agencia'] == codigo:
            return agencia
    return None

# Calcula o dinheiro total das contas pertencentes à agência
def montante_total_agencia(codigo, contas):
    total = 0.0

    for conta in contas:
        # confere se a conta pertence à agência e soma o saldo
        if conta['codigo_agencia'] == codigo:
            total = total + conta['saldo']
    return total
