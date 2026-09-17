#lista
clientes = []

#funcaozinha q verifica se o cpf ja foi usado pra criar algum cliente, e se o cpf ainda n foi utilizado, vai montar a tupla (nome,cpf) e adiciona na lista, e depois disso retorna a tupla pro main 
def criar_client(nome,cpf):
  if buscar_cliente_por_cpf(cpf) is not None: 
    print("Já existe um cliente cadastrado com esse mesmo CPF")
    return None 
    
    novo_cliente = (nome,cpf)
    clientes.append(nome_cliente)clientes.append(nome_cliente)
    return novo_cliente

#percorre a lista bem na posicao que o cpf ta (posicao 1) e se encontrar, ele devolve a tupla daquele cpf
def buscar_clientes_por_cpf(cpf): 
  for cliente in clientes:
    if cliente[1] == cpf:
      return cliente
      return None
      
#percorre a lista clientes e faz uma listinha com as informacoes das tuplas existentes, nada demais
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
