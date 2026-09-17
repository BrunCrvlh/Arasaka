clientes = []

def criar_client(nome,cpf):
  if buscar_cliente_por_cpf(cpf) is not None: 
    print("Já existe um cliente cadastrado com esse mesmo CPF")
    return None 
    novo_cliente = (nome,cpf)
    clientes.append(nome_cliente)clientes.append(nome_cliente)
    return novo_cliente

def buscar_clientes_por_cpf(cpf): 
  for cliente in clientes:
    if cliente[1] == cpf:
      return cliente
      return None

def listar_clientes ():
  if len(clientes) == 0:
    print("Nenhum cliente cadastrado.")
    return
    
    print("n------- CLIENTES -------")
    for cliente in clientes: 
      nome = cliente[0]
      cpf = cliente[1]
      print ("nome:", nome, " CPF:", cpf)
      print("---------------------------")
