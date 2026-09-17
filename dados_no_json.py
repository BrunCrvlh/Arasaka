import json

def salvar_dados_gerais_do_banco (clientes, agencias, contas):
  with open("dados.json", "w") as arquivo:
    json.dump([clientes, agencias, contas], arquivo) 
