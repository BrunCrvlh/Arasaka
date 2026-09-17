clientes = []

def criar_client(nome,cpf):
  if buscar_cliente_por_cpf(cpf) is not None: 
    print("Já existe um cliente cadastrado com esse mesmo CPF")
    return None

novo_cliente = (nome,cpf)
clientes.append(nome_cliente)
return novo_cliente

def buscar
