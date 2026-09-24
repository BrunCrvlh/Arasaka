from menu import menu
from dados_no_json import (salvar_dados_gerais_do_banco, carrega_dados_gerais_do_banco)
            
menu()

salvar_dados_gerais_do_banco()
print("Sessão encerrada.")
