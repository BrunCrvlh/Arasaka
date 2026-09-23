import json

def salvar_dados_gerais_do_banco(clientes, agencias, contas):
   with open("dados.json", "w") as arquivo:
        json.dump([clientes, agencias, contas], arquivo)

def carrega_dados_gerais_do_banco():
    with open("dados.json", "r") as arquivo:
        dados = json.load(arquivo)
        clientes = [tuple(c) for c in dados[0]]
        agencias = [tuple(a) for a in dados[1]]
        contas = [tuple(c) for c in dados[2]]
        return clientes, agencias, contas
