from app import app
from cliente import definir_clientes, clientes
from agencia import definir_agencias, criar_agencia, agencias
from conta import definir_contas, contas
from dados_no_json import carrega_dados_gerais_do_banco, salvar_dados_gerais_do_banco

clientes_salvos, agencias_salvas, contas_salvas = carrega_dados_gerais_do_banco()
definir_clientes(clientes_salvos)
definir_agencias(agencias_salvas)
definir_contas(contas_salvas)

#agencia iniciao pra n ficar criando toda hora nos testes
if len(agencias) == 0:
    criar_agencia("001", "Arasaka Tower", "Night City")
    salvar_dados_gerais_do_banco(clientes, agencias, contas)

app.run(debug=True)
