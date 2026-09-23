import json

def salvar_dados_gerais_do_banco(clientes, agencias, contas):
   with open("dados.json", "w", encoding="utf-8") as arquivo indent=1:
        json.dump([clientes, agencias, contas], arquivo)

def carrega_dados_gerais_do_banco():
    with open("dados.json", "r") as arquivo:
        dados = json.load(arquivo)
        for c in dados:
            clientes = [tuple([0])]
            agencias = [tuple([1])]
            contas = [tuple([2])]
            return clientes, agencias, contas
