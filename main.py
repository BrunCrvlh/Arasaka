from menu import menu
from cliente import definir_clientes
from agencia import definir_agencias
from conta import definir_contas
from dados_no_json import (salvar_dados_gerais_do_banco, carrega_dados_gerais_do_banco)

clientes_salvos, agencias_salvas, contas_salvas = carrega_dados_gerais_do_banco()
definir_clientes(clientes_salvos)
definir_agencias(agencias_salvas)
definir_contas(contas_salvas)
            
menu()

salvar_dados_gerais_do_banco()
print("Sessão encerrada.")
