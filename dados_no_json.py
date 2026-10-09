import json

def salvar_dados_gerais_do_banco(clientes, agencias, contas):
   with open("dados.json", "w", encoding="utf-8") as arquivo:
        json.dump([clientes, agencias, contas], arquivo, indent=1, ensure_ascii=False)

def carrega_dados_gerais_do_banco():
    if not os.path.exists("dados.json") or os.path.getsize("dados.json") == 0:
       return [], [], []

    with open ("dados.json", "r", encoding="utf-8") as arquivo:
       clientes, agencias, contas= json.load(arquivo)
       return clientes, agencias, contas
