import json

def salvar_dados_gerais_do_banco(clientes, agencias, contas):
   with open("dados.json", "w", encoding="utf-8") as arquivo:
        json.dump([clientes, agencias, contas], arquivo) indent=1

def carrega_dados_gerais_do_banco():
    with open("dados.json", "r") as arquivo:
        dados = json.load(arquivo)
        clientes = []
        agencias = []
        contas = []
       
        for cliente in dados[0]:
            clientes.append(tuple(cliente))
        for agencia in dados[1]:
            agencias.append(tuple(agencia))
        for conta in dados[2]:
            contas.append(tuple(conta))
        return clientes, agencias, contas
