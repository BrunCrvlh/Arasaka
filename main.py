from menu import menu
from dados_no_json.py import salvar_dados_gerais_do_banco
            
menu()

print("Sessão encerrada.")            
salvar_dados_gerais_do_banco(clientes, agencias, contas)
